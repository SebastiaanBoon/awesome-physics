# Open Standards and Licenses

Awesome Physics follows established open standards for content, code, data, and
documentation. This page documents which standards the project uses and why.

## Content license: Creative Commons Attribution 4.0 (CC BY 4.0)

The list itself (the prose in `README.md` and the documentation) is released
under **CC BY 4.0**.

- Full legal text: [`LICENSE-CC-BY-4.0.txt`](LICENSE-CC-BY-4.0.txt)
- Human-readable summary: <https://creativecommons.org/licenses/by/4.0/>
- SPDX identifier: `CC-BY-4.0`

CC BY 4.0 lets anyone share and adapt the material for any purpose, including
commercially, provided they give appropriate credit, link to the license, and
indicate if changes were made. It is the recommended license for curated lists
that want attribution.

## Code license: GNU General Public License v3.0 or later (GPL-3.0-or-later)

Scripts, the Makefiles, and CI configuration are free software licensed under
the **GNU General Public License, version 3 or later**.

- Full legal text: [`LICENSE-GPL-3.0.txt`](LICENSE-GPL-3.0.txt)
- License home: <https://www.gnu.org/licenses/gpl-3.0.html>
- SPDX identifier: `GPL-3.0-or-later`

The GPL guarantees the four freedoms (run, study, share, and modify) and
requires derivative works to stay free. Every script carries an
`SPDX-License-Identifier: GPL-3.0-or-later` header.

The current scripts depend only on the Python standard library, distributed
under the Python Software Foundation (PSF) License, so no third-party copyleft
obligations apply. Any library added later keeps its own license; pick
dependencies whose licenses are compatible with the GPL and list them here.

## Open source and open access definitions

Entries are labelled according to widely used definitions:

| Label | Standard |
| :-- | :-- |
| `[OS]` | [Open Source Initiative](https://opensource.org/osd) definition, or open hardware under a recognized open hardware license. |
| `[OA]` | [Budapest Open Access Initiative](https://www.budapestopenaccessinitiative.org/) / [Berlin Declaration](https://openaccess.mpg.de/Berlin-Declaration) definition of open access. |
| `[CC]` | Content published under a [Creative Commons](https://creativecommons.org/licenses/) license. |
| `[Free]` | Free of charge ("gratis") but not necessarily open. |
| `[Freemium]` | A usable free tier with paid upgrades. |
| `[Data]` | A public dataset, archive, or API, usually via an open data license. |
| `[RSS]` | Provides an RSS or Atom feed for syndication. |

## Data and syndication standards

- **RSS 2.0** and **Atom** — feed formats for news and preprint alerts.
- **OPML 2.0** — the format of [`feeds.opml`](feeds.opml), importable by feed readers.
- **JSON** — the format of [`resources.json`](resources.json), a machine-readable
  catalogue of the list.
- **SPDX** — license identifiers used in file headers and metadata.

## Hardware standards

Open hardware entries follow the
[CERN Open Hardware Licence](https://ohwr.org/cern_ohl_s_v2.txt) family or an
equivalent recognized license, and the
[Open Source Hardware Association](https://www.oshwa.org/) definition where an
OSHW certification mark is present.

## Adding a new resource: which label?

1. Is the source code, design, or data openly licensed and modifiable? Use `[OS]`
   and, if the license is a Creative Commons one, also `[CC]`.
2. Is it free to read but not necessarily modifiable? Use `[OA]` and, when the
   license is known, `[CC]`.
3. Is it simply free of charge? Use `[Free]`.
4. Does it have a free tier with paid extras? Use `[Freemium]`.
5. Is it a dataset or API? Add `[Data]`.
6. Does it publish a feed? Add `[RSS]`.

When in doubt, open an issue and ask.
