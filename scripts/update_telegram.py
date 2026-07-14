#!/usr/bin/env python3
"""Fetch the latest public Telegram channel post and write a compact JSON feed."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

CHANNEL = "kubertat"
CHANNEL_URL = f"https://t.me/s/{CHANNEL}"
OUTPUT = Path("telegram-latest.json")


def parse_count(value: str | None) -> int | None:
    if not value:
        return None
    text = value.strip().replace("\u00a0", "").replace(" ", "").replace(",", ".")
    match = re.search(r"(\d+(?:\.\d+)?)\s*([KMB]?)", text, re.IGNORECASE)
    if not match:
        return None
    number = float(match.group(1))
    suffix = match.group(2).upper()
    multiplier = {"": 1, "K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
    return int(number * multiplier)


def text_from(node) -> str:
    return node.get_text("\n", strip=True) if node else ""


def first_count(root, selectors: list[str]) -> int | None:
    for selector in selectors:
        node = root.select_one(selector)
        value = parse_count(text_from(node))
        if value is not None:
            return value
    return None


def reaction_count(root) -> int | None:
    container = root.select_one(".tgme_widget_message_reactions")
    if not container:
        return None
    values: list[int] = []
    for selector in (
        ".tgme_reaction_count",
        ".tgme_widget_message_reaction_count",
        "[class*='reaction'][class*='count']",
        "[class*='reaction'] [class*='count']",
    ):
        for node in container.select(selector):
            value = parse_count(text_from(node))
            if value is not None:
                values.append(value)
    if values:
        return sum(values)
    numbers = [parse_count(part) for part in re.findall(r"\d+(?:[.,]\d+)?[KMB]?", text_from(container), re.I)]
    numbers = [value for value in numbers if value is not None]
    return sum(numbers) if numbers else None


def photo_url(root) -> str | None:
    node = root.select_one(".tgme_widget_message_photo_wrap")
    if not node:
        return None
    style = node.get("style", "")
    match = re.search(r"background-image\s*:\s*url\(['\"]?([^'\")]+)", style)
    return urljoin(CHANNEL_URL, match.group(1)) if match else None


def fetch_latest() -> dict:
    response = requests.get(
        CHANNEL_URL,
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    messages = soup.select(".tgme_widget_message_wrap")
    if not messages:
        raise RuntimeError(f"Telegram preview page contains no public messages; html_size={len(response.text)}")

    wrapper = messages[-1]
    root = wrapper.select_one(".tgme_widget_message") or wrapper
    post_id = root.get("data-post")
    if not post_id:
        raise RuntimeError("Latest Telegram message has no data-post attribute")

    text = text_from(root.select_one(".tgme_widget_message_text"))
    if not text:
        text = text_from(root.select_one(".tgme_widget_message_caption"))

    time_node = root.select_one("time")
    published_at = time_node.get("datetime") if time_node else None

    return {
        "channel": CHANNEL,
        "post": post_id,
        "url": f"https://t.me/{post_id}",
        "text": text,
        "published_at": published_at,
        "views": first_count(root, [".tgme_widget_message_views"]),
        "comments": first_count(root, [".tgme_widget_message_comments", "a[href*='?comment=']"]),
        "reactions": reaction_count(root),
        "forwards": first_count(
            root,
            [
                ".tgme_widget_message_forwards",
                ".tgme_widget_message_shares",
                "[class*='forward'][class*='count']",
                "[class*='share'][class*='count']",
            ],
        ),
        "image": photo_url(root),
        "error": None,
    }


def main() -> None:
    try:
        payload = fetch_latest()
    except Exception as exc:
        # Keep the previous successful snapshot and avoid an hourly commit loop.
        if OUTPUT.exists():
            print(f"Telegram sync failed; keeping existing snapshot: {type(exc).__name__}: {exc}")
            return
        payload = {
            "channel": CHANNEL,
            "post": None,
            "url": f"https://t.me/{CHANNEL}",
            "text": "Open the Telegram channel to read the latest post.",
            "published_at": None,
            "views": None,
            "comments": None,
            "reactions": None,
            "forwards": None,
            "image": None,
            "error": f"{type(exc).__name__}: {exc}",
        }

    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
