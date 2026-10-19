#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build a static, self-contained website from dev/resources.json.

Usage:
    python3 dev/scripts/build_site.py --output _site/index.html

The generated page has no external dependencies: it works offline from any
static host, including GitHub Pages.
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "dev" / "resources.json"
DEFAULT_OUTPUT = ROOT / "_site" / "index.html"
REPO_URL = "https://github.com/dionarley/awesome-physics"

TAG_ORDER = ["OS", "OA", "CC", "Free", "Freemium", "Data", "RSS"]
TAG_LABELS = {
    "OS": "Open source",
    "OA": "Open access",
    "CC": "Creative Commons",
    "Free": "Free",
    "Freemium": "Freemium",
    "Data": "Data / API",
    "RSS": "RSS feed",
}

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E"
    "%3Ctext y='.9em' font-size='90'%3E%E2%9A%9B%EF%B8%8F%3C/text%3E%3C/svg%3E"
)


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_card(resource: dict) -> str:
    tags = [tag for tag in resource.get("tags", []) if tag in TAG_LABELS]
    tags_html = "".join(
        f'<span class="tag tag-{esc(tag.lower())}" title="{esc(TAG_LABELS[tag])}">{esc(tag)}</span>'
        for tag in tags
    )
    search_blob = f"{resource['name']} {resource.get('description', '')} {' '.join(tags)}".lower()
    return (
        f'<article class="card" data-tags="{esc(" ".join(tags))}" '
        f'data-search="{esc(search_blob)}">'
        f'<h3 class="card-title"><a href="{esc(resource["url"])}" '
        f'target="_blank" rel="noopener">{esc(resource["name"])}</a></h3>'
        f'<p class="card-desc">{esc(resource.get("description", ""))}</p>'
        f'<div class="card-tags">{tags_html}</div>'
        f"</article>"
    )


def build(source: pathlib.Path) -> str:
    data = json.loads(source.read_text(encoding="utf-8"))
    sections = data["sections"]
    total = data["count"]
    tag_counts: dict[str, int] = {tag: 0 for tag in TAG_ORDER}
    for section in sections:
        for resource in section["resources"]:
            for tag in resource.get("tags", []):
                if tag in tag_counts:
                    tag_counts[tag] += 1

    nav_html = "".join(
        f'<li><a href="#{esc(section["slug"])}">{esc(section["title"])}'
        f'<span class="count">{len(section["resources"])}</span></a></li>'
        for section in sections
    )

    filter_html = "".join(
        f'<button class="tagbtn" data-tag="{esc(tag)}">{esc(TAG_LABELS[tag])}'
        f'<span class="count">{tag_counts[tag]}</span></button>'
        for tag in TAG_ORDER
    )

    sections_html = []
    for section in sections:
        cards = "".join(render_card(resource) for resource in section["resources"])
        sections_html.append(
            f'<section class="section" id="{esc(section["slug"])}">'
            f'<h2>{esc(section["title"])}<span class="count">{len(section["resources"])}</span></h2>'
            f'<div class="grid">{cards}</div>'
            f"</section>"
        )

    generated = dt.date.today().isoformat()
    licenses = data.get("license", {})

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Awesome Physics</title>
<meta name="description" content="A curated list of {total} open, free, and freemium physics resources: learning, research, data, RSS feeds, forums, and tools.">
<meta property="og:title" content="Awesome Physics">
<meta property="og:description" content="A curated list of {total} open, free, and freemium physics resources.">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<style>
:root {{
  --bg: #0f1220;
  --panel: #171a2b;
  --panel-2: #1e2238;
  --text: #e8eaf6;
  --muted: #9aa0c0;
  --accent: #6ea8fe;
  --accent-2: #b388ff;
  --border: #2a2f4a;
  --radius: 12px;
}}
@media (prefers-color-scheme: light) {{
  :root {{
    --bg: #f6f7fb;
    --panel: #ffffff;
    --panel-2: #eef1f8;
    --text: #171a2b;
    --muted: #5b6178;
    --accent: #2b5fd9;
    --accent-2: #7b3fe4;
    --border: #dfe3ee;
  }}
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
header.hero {{
  padding: 3rem 1.25rem 2rem;
  background: radial-gradient(1200px 400px at 20% -20%, rgba(110,168,254,.25), transparent),
              radial-gradient(900px 400px at 90% -30%, rgba(179,136,255,.22), transparent);
  border-bottom: 1px solid var(--border);
}}
.hero-inner {{ max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: clamp(2rem, 5vw, 3rem); margin: 0 0 .5rem; letter-spacing: -.02em; }}
h1 .emoji {{ -webkit-text-fill-color: initial; }}
.subtitle {{ color: var(--muted); max-width: 70ch; margin: 0 0 1rem; }}
.hero-links {{ display: flex; flex-wrap: wrap; gap: .6rem; }}
.btn {{
  display: inline-block; padding: .5rem .85rem; border: 1px solid var(--border);
  border-radius: 999px; background: var(--panel); color: var(--text); font-size: .9rem;
}}
.btn:hover {{ text-decoration: none; border-color: var(--accent); color: var(--accent); }}
.layout {{ max-width: 1100px; margin: 0 auto; padding: 1.5rem 1.25rem 4rem; display: grid; gap: 2rem; }}
@media (min-width: 900px) {{ .layout {{ grid-template-columns: 260px 1fr; align-items: start; }} }}
aside {{ position: sticky; top: 1rem; max-height: calc(100vh - 2rem); overflow: auto; }}
aside h2, .controls h2 {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); }}
nav ul {{ list-style: none; margin: 0; padding: 0; }}
nav a {{ display: flex; justify-content: space-between; gap: .5rem; padding: .3rem .5rem; border-radius: 8px; color: var(--text); font-size: .9rem; }}
nav a:hover {{ background: var(--panel-2); text-decoration: none; }}
.count {{ color: var(--muted); font-size: .8rem; font-variant-numeric: tabular-nums; }}
.controls {{ margin-bottom: 1.5rem; }}
#q {{
  width: 100%; padding: .8rem 1rem; font-size: 1rem; color: var(--text);
  background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius); outline: none;
}}
#q:focus {{ border-color: var(--accent); box-shadow: 0 0 0 3px rgba(110,168,254,.2); }}
.tagbtns {{ display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .75rem; }}
.tagbtn {{
  cursor: pointer; padding: .3rem .7rem; border-radius: 999px; font-size: .82rem;
  border: 1px solid var(--border); background: var(--panel); color: var(--muted);
  display: inline-flex; align-items: center; gap: .35rem;
}}
.tagbtn.active {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
.tagbtn.active .count {{ color: rgba(255,255,255,.85); }}
.result {{ color: var(--muted); font-size: .9rem; margin: .75rem 0 0; }}
.section {{ margin-bottom: 2.5rem; scroll-margin-top: 1rem; }}
.section h2 {{ font-size: 1.35rem; border-bottom: 1px solid var(--border); padding-bottom: .4rem; }}
.section h2 .count {{ margin-left: .5rem; font-weight: 400; }}
.grid {{ display: grid; gap: .85rem; }}
@media (min-width: 640px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
.card {{
  background: var(--panel); border: 1px solid var(--border); border-radius: var(--radius);
  padding: .9rem 1rem; transition: border-color .15s, transform .15s;
}}
.card:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
.card-title {{ margin: 0 0 .35rem; font-size: 1rem; }}
.card-desc {{ margin: 0 0 .6rem; color: var(--muted); font-size: .9rem; }}
.card-tags {{ display: flex; flex-wrap: wrap; gap: .3rem; }}
.tag {{ font-size: .7rem; padding: .12rem .5rem; border-radius: 999px; border: 1px solid var(--border); color: var(--muted); }}
.tag-os {{ color: #4ade80; border-color: #4ade8055; }}
.tag-oa {{ color: #38bdf8; border-color: #38bdf855; }}
.tag-cc {{ color: #f472b6; border-color: #f472b655; }}
.tag-free {{ color: #fbbf24; border-color: #fbbf2455; }}
.tag-freemium {{ color: #a78bfa; border-color: #a78bfa55; }}
.tag-data {{ color: #22d3ee; border-color: #22d3ee55; }}
.tag-rss {{ color: #fb923c; border-color: #fb923c55; }}
.no-results {{ display: none; color: var(--muted); padding: 2rem 0; }}
body.filtered .no-results.visible {{ display: block; }}
footer {{ border-top: 1px solid var(--border); padding: 1.5rem 1.25rem; color: var(--muted); font-size: .85rem; }}
footer .inner {{ max-width: 1100px; margin: 0 auto; display: flex; flex-wrap: wrap; gap: .5rem 1.5rem; justify-content: space-between; }}
</style>
</head>
<body>
<header class="hero">
  <div class="hero-inner">
    <h1><span class="emoji">⚛️</span> Awesome Physics</h1>
    <p class="subtitle">A curated list of <strong>{total}</strong> open, free, and freemium physics resources:
    learning, research, data, RSS feeds, forums, and tools.</p>
    <div class="hero-links">
      <a class="btn" href="{REPO_URL}">GitHub repository</a>
      <a class="btn" href="{REPO_URL}/blob/main/README.md">README</a>
      <a class="btn" href="{REPO_URL}/blob/main/dev/feeds.opml">RSS / OPML</a>
      <a class="btn" href="{REPO_URL}/blob/main/CONTRIBUTING.md">Contribute</a>
    </div>
  </div>
</header>
<div class="layout">
  <aside>
    <h2>Sections</h2>
    <nav><ul>{nav_html}</ul></nav>
  </aside>
  <main>
    <div class="controls">
      <input id="q" type="search" placeholder="Search {total} resources…" autocomplete="off" aria-label="Search resources">
      <div class="tagbtns">
        <button class="tagbtn active" data-tag="all">All<span class="count">{total}</span></button>
        {filter_html}
      </div>
      <p class="result" id="result">{total} resources</p>
    </div>
    <p class="no-results" id="noresults">No resources match your search.</p>
    {"".join(sections_html)}
  </main>
</div>
<footer>
  <div class="inner">
    <span>Content: <a href="{REPO_URL}/blob/main/LICENSE">CC BY 4.0</a> · Code: <a href="{REPO_URL}/blob/main/LICENSE-CODE">GPL-3.0-or-later</a></span>
    <span>Generated from <a href="{REPO_URL}/blob/main/README.md">README.md</a> on {generated} · source: {esc(licenses.get("content", "CC-BY-4.0"))} / {esc(licenses.get("code", "GPL-3.0-or-later"))}</span>
  </div>
</footer>
<script>
const q = document.getElementById('q');
const cards = Array.from(document.querySelectorAll('.card'));
const sections = Array.from(document.querySelectorAll('.section'));
const buttons = Array.from(document.querySelectorAll('.tagbtn'));
const result = document.getElementById('result');
const noresults = document.getElementById('noresults');
let active = 'all';

function apply() {{
  const term = q.value.trim().toLowerCase();
  let shown = 0;
  for (const card of cards) {{
    const matchQuery = !term || card.dataset.search.includes(term);
    const matchTag = active === 'all' || card.dataset.tags.split(' ').includes(active);
    const visible = matchQuery && matchTag;
    card.hidden = !visible;
    if (visible) shown++;
  }}
  for (const section of sections) {{
    const any = section.querySelector('.card:not([hidden])');
    section.hidden = !any;
  }}
  result.textContent = shown + (shown === 1 ? ' resource' : ' resources');
  noresults.classList.toggle('visible', shown === 0);
  document.body.classList.toggle('filtered', true);
}}

q.addEventListener('input', apply);
for (const button of buttons) {{
  button.addEventListener('click', () => {{
    active = button.dataset.tag;
    for (const other of buttons) other.classList.toggle('active', other === button);
    apply();
  }});
}}
</script>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build(pathlib.Path(args.source)), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
