#!/usr/bin/env python3
"""Fetch the latest Telegram channel post through MTProto."""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.sessions import StringSession

CHANNEL = "kubertat"
OUTPUT = Path("telegram-latest.json")
IMAGE = Path("telegram-latest.jpg")
TEMP_IMAGE = Path("telegram-latest.tmp.jpg")


def required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def reaction_count(message) -> int | None:
    reactions = getattr(message, "reactions", None)
    results = getattr(reactions, "results", None)
    if not results:
        return None
    return sum(int(result.count) for result in results)


def comment_count(message) -> int | None:
    replies = getattr(message, "replies", None)
    count = getattr(replies, "replies", None)
    return int(count) if count is not None else None


def comparable(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if key != "updated_at"}


def existing_payload() -> dict | None:
    if not OUTPUT.exists():
        return None
    try:
        return json.loads(OUTPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def replace_image_if_changed(temp_path: Path) -> bool:
    if not temp_path.exists():
        return False
    if IMAGE.exists() and IMAGE.read_bytes() == temp_path.read_bytes():
        temp_path.unlink()
        return False
    temp_path.replace(IMAGE)
    return True


async def fetch_latest() -> dict:
    api_id = int(required_env("TG_API_ID"))
    api_hash = required_env("TG_API_HASH")
    session = required_env("TG_SESSION")

    client = TelegramClient(StringSession(session), api_id, api_hash)
    await client.connect()
    try:
        if not await client.is_user_authorized():
            raise RuntimeError("TG_SESSION is not authorized")

        entity = await client.get_entity(CHANNEL)
        messages = await client.get_messages(entity, limit=20)
        message = next(
            (
                item
                for item in messages
                if item.id and not item.action and (item.message or item.media)
            ),
            None,
        )
        if message is None:
            raise RuntimeError("Telegram channel contains no regular posts")

        image_path: str | None = None
        if message.photo:
            TEMP_IMAGE.unlink(missing_ok=True)
            downloaded = await message.download_media(file=str(TEMP_IMAGE))
            if downloaded:
                replace_image_if_changed(Path(downloaded))
                image_path = IMAGE.as_posix()
        elif IMAGE.exists():
            IMAGE.unlink()

        return {
            "channel": CHANNEL,
            "post": f"{CHANNEL}/{message.id}",
            "url": f"https://t.me/{CHANNEL}/{message.id}",
            "text": message.message or "",
            "published_at": message.date.isoformat() if message.date else None,
            "views": int(message.views) if message.views is not None else None,
            "comments": comment_count(message),
            "reactions": reaction_count(message),
            "forwards": int(message.forwards) if message.forwards is not None else None,
            "image": image_path,
            "error": None,
        }
    finally:
        await client.disconnect()
        TEMP_IMAGE.unlink(missing_ok=True)


async def main() -> None:
    try:
        payload = await fetch_latest()
    except Exception as exc:
        # Keep the last successful snapshot if Telegram is temporarily unavailable.
        if OUTPUT.exists():
            print(f"Telegram sync failed; keeping existing snapshot: {type(exc).__name__}: {exc}")
            return
        raise

    previous = existing_payload()
    if previous is not None and comparable(previous) == comparable(payload):
        print("Telegram feed is unchanged")
        return

    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated Telegram feed from {payload['url']}")


if __name__ == "__main__":
    asyncio.run(main())
