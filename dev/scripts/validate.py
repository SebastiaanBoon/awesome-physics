#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Validate the structure of a README.

Checks performed:
  * exactly one level-1 heading;
  * a table-of-contents section exists;
  * every table-of-contents anchor matches a real heading;
  * every resource entry has at least one known label;
  * descriptions start with a capital letter and end with a period;
  * no duplicate URLs.

Usage:
    python3 dev/scripts/validate.py [--readme README.pt-BR.md]
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_README = ROOT / "README.md"

HEADINGS = re.compile(r"^(?P<level>#+)\s+(?P<title>.+?)\s*$")
TOC_LINK = re.compile(r"^\s*-\s+\[(?P<text>[^\]]+)\]\(#(?P<anchor>[^)]+)\)\s*$")
ENTRY = re.compile(
    r"^\s*-\s+\[(?P<name>[^\]]+)\]\((?P<url>[^)]+)\)"
    r"\s*[-–—]\s*(?P<description>.*?)\s*$"
)
TAG = re.compile(r"`\[(?P<tag>[A-Za-z]+)\]`")

KNOWN_TAGS = {"OS", "OA", "CC", "Free", "Freemium", "Data", "RSS"}

# Sections that wrap the list rather than contain resources; both the English
# and the Portuguese titles are recognised so the validator is language-neutral.
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

# Titles of the table-of-contents section.
TOC_SECTIONS = {"Contents", "Conteúdo"}


def slugify(title: str) -> str:
    slug = title.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--readme",
        default=str(DEFAULT_README),
        help="README file to validate.",
    )
    args = parser.parse_args()

    readme = pathlib.Path(args.readme)
    errors: list[str] = []
    warnings: list[str] = []

    text = readme.read_text(encoding="utf-8")
    lines = text.splitlines()

    h1 = [ln for ln in lines if re.match(r"^#\s+\S", ln)]
    if len(h1) != 1:
        errors.append(f"Expected exactly one level-1 heading, found {len(h1)}.")

    headings: list[str] = []
    current_section: str | None = None
    toc_anchors: list[str] = []
    in_toc = False
    seen_urls: dict[str, str] = {}
    entry_count = 0

    for number, line in enumerate(lines, start=1):
        heading = HEADINGS.match(line)
        if heading:
            level = len(heading.group("level"))
            title = heading.group("title").strip()
            if level == 2:
                headings.append(title)
                current_section = None if title in NON_RESOURCE_SECTIONS else title
                in_toc = title in TOC_SECTIONS
            continue

        if in_toc:
            toc = TOC_LINK.match(line)
            if toc:
                toc_anchors.append(toc.group("anchor"))
            continue

        if current_section is None:
            continue

        entry = ENTRY.match(line)
        if not entry:
            if line.strip().startswith("- ["):
                errors.append(f"Line {number}: malformed entry: {line.strip()}")
            continue

        entry_count += 1
        name = entry.group("name")
        url = entry.group("url")
        description = entry.group("description")

        tags = TAG.findall(description)
        if not tags:
            errors.append(f"Line {number}: entry '{name}' has no label.")
        unknown = set(tags) - KNOWN_TAGS
        if unknown:
            errors.append(
                f"Line {number}: entry '{name}' uses unknown labels: {sorted(unknown)}"
            )

        prose = TAG.sub("", description).strip()
        if not prose:
            errors.append(f"Line {number}: entry '{name}' has no description.")
        else:
            if not prose[-1] in ".!?":
                errors.append(f"Line {number}: description of '{name}' does not end with punctuation.")
            if not prose[0].isupper() and not prose[0].isdigit():
                warnings.append(f"Line {number}: description of '{name}' does not start with a capital.")

        if url in seen_urls:
            errors.append(f"Line {number}: duplicate URL {url} (also at {seen_urls[url]}).")
        else:
            seen_urls[url] = f"line {number}"

        if not url.startswith("https://"):
            warnings.append(f"Line {number}: '{name}' does not use https: {url}")

    expected = [slugify(title) for title in headings if title not in TOC_SECTIONS]
    missing = [anchor for anchor in expected if anchor not in toc_anchors]
    extra = [anchor for anchor in toc_anchors if anchor not in expected]
    for anchor in missing:
        errors.append(f"Table of contents is missing an entry for '#{anchor}'.")
    for anchor in extra:
        errors.append(f"Table of contents links to unknown section '#{anchor}'.")

    for warning in warnings:
        print(f"warning: {warning}")
    for error in errors:
        print(f"error: {error}")

    print(f"\nChecked {entry_count} entries across {len(headings)} sections.")
    if errors:
        print(f"FAILED with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1
    print(f"OK with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
