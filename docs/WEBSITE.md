# Website

Awesome Physics ships a small static website that presents the list in a
searchable, filterable form.

- **Live site:** <https://dionarley.github.io/awesome-physics/>
- **Source:** [`dev/scripts/build_site.py`](../dev/scripts/build_site.py)
- **Input:** [`dev/resources.json`](../dev/resources.json)
- **Output:** `_site/index.html` (not committed, built in CI)

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

This regenerates `dev/resources.json` and writes `_site/index.html`. Open the
file in a browser, or serve it over HTTP:

```sh
python3 -m http.server -d _site 8000
```

## Deployment

Deployment is automated by
[`.github/workflows/pages.yml`](../.github/workflows/pages.yml) using GitHub
Pages with a workflow build:

1. Regenerate `dev/resources.json` from `README.md`.
2. Build `_site/index.html` and add `.nojekyll`.
3. Upload the artifact and deploy it to GitHub Pages.

The workflow runs on every push to `main` and can also be triggered manually
from the Actions tab.

## Editing the design

Edit the HTML template and CSS inside `build_site.py`, then run `make site` and
open the result. Keep the page free of external assets so it stays fast and
self-contained.
