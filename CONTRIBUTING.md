# Contributing to Awesome Physics

Thanks for taking the time to contribute! This project collects open, free, and
freemium physics resources, and it is improved by people like you.

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) and the
[development guide](dev/README.md) before you start.

## Ways to contribute

- **Add a resource** that is missing and clearly useful.
- **Fix a broken link** or replace a dead project with its successor.
- **Improve a description** so readers understand why the resource matters.
- **Add or correct a label** from the legend (for example `[OS]` or `[Freemium]`).
- **Report a problem** with the list structure, licensing, or tooling.

## Requirements for every entry

1. **Relevance.** The resource must be about physics or directly used by physicists.
2. **Accessibility.** It must be open source, open access, free, or freemium. Fully
   paywalled resources without a usable free tier are out of scope.
3. **Quality.** Prefer canonical, actively maintained resources over dead or obscure ones.
4. **Stability.** Link to the official project page or a stable archive, not a mirror.
5. **Labelling.** Every entry ends with one or more tags from the
   [legend](README.md#legend).
6. **Format.** Use the exact list format:

   ```markdown
   - [Resource Name](https://example.org/) - A short description ending with a period. `[OS]` `[Free]`
   ```

   The link comes first, the description is a sentence that starts with a capital
   letter and ends with a period, and the tags close the line.

## Add a resource

1. Fork the repository and create a branch: `git checkout -b add-my-resource`.
2. Edit `README.md` and place the entry in the most relevant section.
3. Add the same entry to `README.pt-BR.md`, in the same section and position,
   with a Portuguese description. Keep the URL, the name, and the labels
   identical so both lists stay in sync.
4. If the resource provides an RSS or Atom feed, add it to
   `dev/data/feeds.csv` as well.
5. Run the local checks (see the [development guide](dev/README.md)):

   ```sh
   make validate
   make links
   ```

6. Commit with a [Conventional Commit](#commit-messages), for example
   `feat(readme): add QuTiP to the quantum computing section`.
7. Open a pull request whose title follows the same format, and fill in the
   template.

## One entry per pull request

Small, focused pull requests are reviewed faster. If you have many suggestions,
open several pull requests or an issue first.

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

- **type** — one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
  `build`, `ci`, `chore`, `revert`.
- **scope** (optional) — the area touched, for example `readme`, `pt-br`,
  `site`, `scripts`, `data`, `feeds`, `ci`, or `deps`.
- **subject** — imperative mood, lowercase, no trailing period, and at most 72
  characters including the type and scope.
- **body** (optional) — what changed and why, separated from the subject by a
  blank line.
- **footer** (optional) — `BREAKING CHANGE: …`, `Closes #123`, or `Refs #123`.

Examples:

```
feat(readme): add QuTiP to the quantum computing section
fix(pt-br): correct the SciX description
docs: document the release checklist
ci: validate commit messages in pull requests
```

A commit that only adds or removes list entries is usually `feat`; a broken
link or a wrong description is `fix`; changes to `docs/` or to the prose of the
README are `docs`.

Merge commits, reverts, and `fixup!`/`squash!` commits are exempt.

Install the local hook and the message template once per clone:

```sh
make hooks
```

The same checker (`dev/scripts/check_commit.py`) runs in CI for every commit and
for the pull request title, because pull requests are squash-merged.

## Reporting broken links

Open an issue with the [broken link template](.github/ISSUE_TEMPLATE/broken-link.md)
and include the section and the URL. Automated link checking also runs in CI.

## Translations

The list is bilingual and both files are first-class:

- [`README.md`](README.md) — English.
- [`README.pt-BR.md`](README.pt-BR.md) — Português (Brasil).

When you add, change, or remove an entry, do the same in every translation, in
the same section and order. Project names, URLs, and labels stay identical; only
section titles and descriptions are translated. Run `make validate` to check all
translations at once.

To start a new translation, copy `README.md`, translate the section titles, the
introduction, and the descriptions, then run `make validate` and `make resources`.

## Licensing of contributions

By contributing you agree that:

- Your prose contributions to the list are licensed under
  **Creative Commons Attribution 4.0 International (`CC BY 4.0`)**.
- Your code and configuration contributions are licensed under the
  **GNU General Public License, version 3 or later (`GPL-3.0-or-later`)**.

Do not paste content you do not have the right to license this way.

## Style notes

- In `README.md`, write in English (American or British spelling, but be consistent within an entry). In `README.pt-BR.md`, write in Brazilian Portuguese.
- Keep descriptions to one sentence, ideally under 120 characters.
- Do not use marketing language; describe what the resource is.
- Prefer `https://` links.
- Do not add a trailing slash unless the site requires it.
- Keep sections in their existing order and alphabetical only where it already exists.

Thank you for helping make physics more open!
