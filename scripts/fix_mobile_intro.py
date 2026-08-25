from pathlib import Path

path = Path("index.html")
text = path.read_text(encoding="utf-8")
rule = "\n    /* Mobile: decorative PK / SRE label is hidden to avoid overlapping the hero eyebrow. */\n    @media(max-width:680px){.intro::after{display:none}}\n"
if ".intro::after{display:none}" not in text:
    text = text.replace("</style>", rule + "</style>", 1)
    path.write_text(text, encoding="utf-8")
