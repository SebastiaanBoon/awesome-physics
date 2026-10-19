#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""Generate an OPML 2.0 feed file from dev/data/feeds.csv.

Usage:
    python3 dev/scripts/generate_opml.py [--input dev/data/feeds.csv] [--output dev/feeds.opml]
"""

from __future__ import annotations

import argparse
import csv
import html
import pathlib
from collections import OrderedDict

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_INPUT = ROOT / "dev" / "data" / "feeds.csv"
DEFAULT_OUTPUT = ROOT / "dev" / "feeds.opml"

HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="2.0">
  <head>
    <title>Awesome Physics - RSS and Atom feeds</title>
    <dateCreated>{date}</dateCreated>
    <ownerName>Awesome Physics contributors</ownerName>
    <ownerEmail>awesome-physics@example.org</ownerEmail>
  </head>
  <body>
"""

FOOT = """  </body>
</opml>
"""


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument(
        "--date",
        default="Mon, 19 Oct 2026 00:00:00 GMT",
        help="Value for the OPML dateCreated element.",
    )
    args = parser.parse_args()

    with open(args.input, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    grouped: "OrderedDict[str, list[dict]]" = OrderedDict()
    for row in rows:
        category = (row.get("category") or "Uncategorised").strip()
        grouped.setdefault(category, []).append(row)

    lines = [HEAD.format(date=esc(args.date))]
    for category, items in grouped.items():
        lines.append(f'    <outline text="{esc(category)}" title="{esc(category)}">\n')
        for item in items:
            title = esc((item.get("title") or "").strip())
            xml_url = esc((item.get("url") or "").strip())
            html_url = esc((item.get("htmlUrl") or "").strip())
            lines.append(
                f'      <outline type="rss" text="{title}" title="{title}" '
                f'xmlUrl="{xml_url}" htmlUrl="{html_url}" />\n'
            )
        lines.append("    </outline>\n")
    lines.append(FOOT)

    out = pathlib.Path(args.output)
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {len(rows)} feeds in {len(grouped)} categories to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
