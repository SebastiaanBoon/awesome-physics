# Website

Awesome Physics ships a small static website that presents the list in a
searchable, filterable form.

- **Live site:** <https://dionarley.github.io/awesome-physics/>
- **Source:** [`dev/scripts/build_site.py`](../dev/scripts/build_site.py)
- **Input:** [`dev/resources.json`](../dev/resources.json)
- **Output:** [`docs/index.html`](index.html) (committed)

## How it works

`build_site.py` reads the generated catalogue and renders a single
self-contained `index.html` with embedded CSS and JavaScript. There are no
external dependencies, so the page works offline and from any static host.

Features:

- Full-text search over names and descriptions.
- Filtering by label (`OS`, `OA`, `CC`, `Free`, `Freemium`, `Data`, `RSS`).
- Section navigation with per-section counts.
- Responsive layout with light and dark themes.

## Build locally

```sh
make site
```

This regenerates `dev/resources.json`, writes `docs/index.html`, and adds
`docs/.nojekyll`. Open the file in a browser, or serve it over HTTP:

```sh
python3 -m http.server -d docs 8000
```

## Deployment

The site is published with **GitHub Pages** using the classic "deploy from a
branch" mode:

- **Branch:** `main`
- **Folder:** `/docs`

GitHub Pages rebuilds automatically on every push to `main`, so no CI runner is
involved. The generated `docs/index.html` is committed together with the README
change.

## Keeping the site in sync

Whenever `README.md` or `dev/data/feeds.csv` change, regenerate the site and
commit the result:

```sh
make all     # resources + opml + validate
make site    # rebuild docs/index.html
git add docs/index.html
```

If the site is ever out of date, `make site` fixes it. The validator does not
check the website, so a maintainer must remember this step when reviewing pull
requests that add resources.

## Editing the design

Edit the HTML template and CSS inside `build_site.py`, then run `make site` and
open the result. Keep the page free of external assets so it stays fast and
self-contained.
