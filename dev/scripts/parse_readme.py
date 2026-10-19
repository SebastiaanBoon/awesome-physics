#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Parse a README into a structured JSON catalogue.

Usage:
    python3 dev/scripts/parse_readme.py [--input README.md] [--output dev/resources.json]

The same script handles every translation of the list; the language only
changes the catalogue description and the ``generated_from`` field.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "README.md"

HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
ENTRY_RE = re.compile(
    r"^\s*-\s+\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)"
    r"(?:\s*[-–—]\s*(?P<description>.*?))?\s*$"
)
TAG_RE = re.compile(r"`\[(?P<tag>[A-Za-z]+)\]`")

# Titles of the sections that wrap the list instead of containing resources.
# Both the English and the Portuguese headings are listed so the parser works
# for every translation.
NON_RESOURCE_SECTIONS = {
    "Contents",
    "Legend",
    "Related Awesome Lists",
    "Contributing",
    "License",
    "Conteúdo",
    "Legenda",
    "Listas Awesome Relacionadas",
    "Contribuindo",
    "Licença",
}

DESCRIPTIONS = {
    "en": "Open, free, and freemium physics resources.",
    "pt-BR": "Recursos abertos, gratuitos e freemium de física.",
}


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def parse(readme: pathlib.Path, lang: str) -> dict:
    text = readme.read_text(encoding="utf-8")
    sections: list[dict] = []
    current: dict | None = None

    for line in text.splitlines():
        heading = HEADING_RE.match(line)
        if heading:
            title = heading.group("title").strip()
            if title in NON_RESOURCE_SECTIONS:
                current = None
            else:
                current = {"title": title, "slug": slugify(title), "resources": []}
                sections.append(current)
            continue

        if current is None:
            continue

        entry = ENTRY_RE.match(line)
        if not entry:
            continue

        description = (entry.group("description") or "").strip()
        tags = TAG_RE.findall(description) if description else TAG_RE.findall(line)
        clean_description = TAG_RE.sub("", description).strip()
        clean_description = re.sub(r"\s{2,}", " ", clean_description)

        current["resources"].append(
            {
                "name": entry.group("name").strip(),
                "url": entry.group("url").strip(),
                "description": clean_description,
                "tags": tags,
            }
        )

    total = sum(len(section["resources"]) for section in sections)
    return {
        "name": "awesome-physics",
        "language": lang,
        "description": DESCRIPTIONS.get(lang, DESCRIPTIONS["en"]),
        "license": {
            "content": "CC-BY-4.0",
            "code": "GPL-3.0-or-later",
        },
        "generated_from": readme.name,
        "count": total,
        "sections": sections,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="README file to parse.",
    )
    parser.add_argument("--output", default=str(ROOT / "dev" / "resources.json"))
    parser.add_argument(
        "--lang",
        default="en",
        choices=sorted(DESCRIPTIONS),
        help="Language metadata written into the catalogue.",
    )
    args = parser.parse_args()

    data = parse(pathlib.Path(args.input), args.lang)
    out = pathlib.Path(args.output)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {data['count']} resources in {len(data['sections'])} sections "
        f"to {out} ({args.lang})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
