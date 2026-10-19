# Development Guide

This folder (`dev/`) contains everything you need to develop, validate, and
maintain the Awesome Physics list. It also contains the open licensing standard
used by the project: the **Creative Commons** license texts, in full.

## Layout

```
dev/
├── README.md                     This file.
├── STANDARDS.md                  The open standards and licenses used.
├── checklist.md                  Reviewer and contributor checklist.
├── Makefile                      Common maintenance tasks.
├── feeds.opml                    Generated: importable RSS/Atom feed list.
├── resources.json                Generated: structured catalogue (English).
├── resources.pt-BR.json          Generated: structured catalogue (Portuguese).
├── data/
│   └── feeds.csv                 Source of truth for RSS/Atom feeds.
├── templates/
│   ├── resource.md               Template for a single list entry.
│   ├── section.md                Template for a new section.
├── scripts/
│   ├── parse_readme.py           README -> resources.json
│   ├── generate_opml.py          feeds.csv -> feeds.opml
│   ├── validate.py               Structural checks on a README.
│   ├── check_links.py            HTTP link checker for README.md.
│   ├── check_commit.py           Validate a Conventional Commit message.
│   └── build_site.py             resources.json -> docs/index.html
├── LICENSE-CC-BY-4.0.txt         Full Creative Commons Attribution 4.0 text.
└── LICENSE-GPL-3.0.txt           Full GNU General Public License v3 text.
```

## Translations

The list exists in two languages, and both are first-class:

- `README.md` — English.
- `README.pt-BR.md` — Português (Brasil).

Keep the two files structurally identical: same sections, same entries, same
URLs and labels, in the same order. Only the section titles and the descriptions
are translated. `make validate` checks every translation, and `make resources`
builds one catalogue per translation.

## Requirements

- Python 3.9 or newer (standard library only for the default scripts).
- `make` (optional, for the convenience targets).
- Network access for `check_links.py`.

No third-party Python packages are required. `make links` uses only the standard
library so it works in minimal environments and in CI.

## Common tasks

```sh
make hooks        # install the commit-msg hook and the commit template
make validate     # check the structure and tags of every translation
make resources    # regenerate dev/resources.json and dev/resources.pt-BR.json
make opml         # regenerate dev/feeds.opml from dev/data/feeds.csv
make links        # check every URL in README.md (network required)
make site         # build the static website into docs/
make all          # resources + opml + validate
```

Run a script directly if you prefer:

```sh
python3 dev/scripts/validate.py --readme README.pt-BR.md
python3 dev/scripts/check_links.py --concurrency 16 --timeout 15
```

## Workflow for a change

1. Edit `README.md` and, to keep the translations in sync, `README.pt-BR.md`
   (and `dev/data/feeds.csv` if you add a feed).
2. Run `make all` and `make links`.
3. Run `make site` to refresh the generated website.
4. Commit the README changes and the regenerated artifacts together, using a
   [Conventional Commit](../CONTRIBUTING.md#commit-messages).
5. Open a pull request.

## Adding an RSS or Atom feed

Feeds live in `dev/data/feeds.csv` with the columns:

```csv
title,url,htmlUrl,category
```

- `title` — human-readable feed name.
- `url` — the feed URL (RSS or Atom XML).
- `htmlUrl` — the human-facing website.
- `category` — one of the OPML categories (for example `Physics`, `Astronomy`).

Then regenerate the OPML file:

```sh
make opml
```

The generated `feeds.opml` can be imported into any feed reader.

## Adding a section

1. Add the section to the table of contents in every translation
   (`README.md` and `README.pt-BR.md`), keeping the anchor format produced by
   GitHub (`#lowercase-with-dashes`).
2. Add the `## Section Name` heading in the body of each translation.
3. Add at least three entries before proposing the section.

The validator checks that the table of contents and the headings match.

## Relationship to the main README

`README.md` (English) and `README.pt-BR.md` (Portuguese) are the sources of
truth for list entries. `resources.json`, `resources.pt-BR.json`, `feeds.opml`,
and the generated website in `docs/` are derived artifacts. The catalogues and
the feed list are never edited by hand; the website is regenerated with
`make site` and committed.

## Licensing

- Prose, documentation, and the list: **CC BY 4.0**.
- Scripts, Makefiles, and configuration: **GPL-3.0-or-later**.

Full texts are in this folder. See [STANDARDS.md](STANDARDS.md) for details.
