#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Parse README.md into a structured JSON catalogue.

Usage:
    python3 dev/scripts/parse_readme.py [--output dev/resources.json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
README = ROOT / "README.md"

HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")
ENTRY_RE = re.compile(
    r"^\s*-\s+\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)"
    r"(?:\s*[-–—]\s*(?P<description>.*?))?\s*$"
)
TAG_RE = re.compile(r"`\[(?P<tag>[A-Za-z]+)\]`")

NON_RESOURCE_SECTIONS = {
    "Contents",
    "Legend",
    "Related Awesome Lists",
    "Contributing",
    "License",
}


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def parse() -> dict:
    text = README.read_text(encoding="utf-8")
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
        "description": "Open, free, and freemium physics resources.",
        "license": {
            "content": "CC-BY-4.0",
            "code": "CC0-1.0",
        },
        "generated_from": "README.md",
        "count": total,
        "sections": sections,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default=str(ROOT / "dev" / "resources.json"),
        help="Path of the JSON file to write.",
    )
    args = parser.parse_args()

    data = parse()
    out = pathlib.Path(args.output)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {data['count']} resources in {len(data['sections'])} sections to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
