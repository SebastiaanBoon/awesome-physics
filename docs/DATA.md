# Data Model

`dev/resources.json` (English) and `dev/resources.pt-BR.json` (Portuguese) are
machine-readable catalogues generated from `README.md` and `README.pt-BR.md` by
`dev/scripts/parse_readme.py`. Do not edit them by hand; run `make resources`
instead.

## Top-level object

| Field | Type | Description |
| :-- | :-- | :-- |
| `name` | string | Repository name, `awesome-physics`. |
| `language` | string | BCP 47 language tag (`en`, `pt-BR`). |
| `description` | string | Short description of the list in that language. |
| `license` | object | `content` and `code` SPDX identifiers. |
| `generated_from` | string | The source document (`README.md`). |
| `count` | integer | Total number of resources. |
| `sections` | array | One object per list section. |

## Section object

| Field | Type | Description |
| :-- | :-- | :-- |
| `title` | string | Human-readable section title. |
| `slug` | string | GitHub-style anchor for the section. |
| `resources` | array | The entries in the section. |

## Resource object

| Field | Type | Description |
| :-- | :-- | :-- |
| `name` | string | Display name of the resource. |
| `url` | string | Canonical URL. |
| `description` | string | One-sentence description without tags. |
| `tags` | array of strings | Labels such as `OS`, `OA`, `CC`, `Free`, `Freemium`, `Data`, `RSS`. |

## Example

```json
{
  "name": "QuTiP",
  "url": "https://qutip.org/",
  "description": "Quantum Toolbox in Python for open quantum systems.",
  "tags": ["OS", "Free"]
}
```

## Consumers

Possible uses of the generated catalogue:

- Building a searchable website or static site.
- Generating badges or counters.
- Cross-checking links and labels.
- Producing alternative formats (CSV, BibTeX, JSON-LD).
