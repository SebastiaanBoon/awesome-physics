# Website

Awesome Physics ships a small static website that presents the list in a
searchable, filterable form.

- **Live site:** <https://dionarley.github.io/awesome-physics/>
- **Portuguese site:** <https://dionarley.github.io/awesome-physics/pt-BR/>
- **Source:** [`dev/scripts/build_site.py`](../dev/scripts/build_site.py)
- **Input:** [`dev/resources.json`](../dev/resources.json) (EN) and [`dev/resources.pt-BR.json`](../dev/resources.pt-BR.json) (PT)
- **Output:** [`docs/index.html`](index.html) and `docs/pt-BR/index.html` (committed)

## How it works

`build_site.py` reads a generated catalogue and renders a single
self-contained `index.html` with embedded CSS and JavaScript. There are no
external dependencies, so the page works offline and from any static host.

Features:

- Full-text search over names and descriptions.
- Filtering by label (`OS`, `OA`, `CC`, `Free`, `Freemium`, `Data`, `RSS`).
- Section navigation with per-section counts.
- Responsive layout with light and dark themes.

## Languages

The site is bilingual. `--lang` selects the interface strings and the catalogue
to render:

| Language | Catalogue | Output |
| :-- | :-- | :-- |
| `en` | `dev/resources.json` | `docs/index.html` |
| `pt-BR` | `dev/resources.pt-BR.json` | `docs/pt-BR/index.html` |

Each page has a language switch button in the header that links to the other
language, and an `<link rel="alternate" hreflang>` hint for search engines.

## Build locally

```sh
make site
```

This regenerates both catalogues and writes `docs/index.html`,
`docs/pt-BR/index.html`, and the `docs/.nojekyll` marker. Open the files in a
browser, or serve them over HTTP:

```sh
python3 -m http.server -d docs 8000
```

## Deployment

The site is published with **GitHub Pages** using the classic "deploy from a
branch" mode:

- **Branch:** `main`
- **Folder:** `/docs`

GitHub Pages rebuilds automatically on every push to `main`, so no CI runner is
involved. The generated `docs/index.html` and `docs/pt-BR/index.html` are
committed together with the README changes.

## Keeping the site in sync

Whenever any `README` or `dev/data/feeds.csv` changes, regenerate the site and
commit the result:

```sh
make all     # resources + opml + validate
make site    # rebuild docs/index.html and docs/pt-BR/index.html
git add docs
```

If the site is ever out of date, `make site` fixes it. The validator does not
check the website, so a maintainer must remember this step when reviewing pull
requests that add resources.

## Editing the design

Edit the HTML template and CSS inside `build_site.py`, then run `make site` and
open the result. Keep the page free of external assets so it stays fast and
self-contained.
