# Review Checklist

Use this checklist when adding a resource or reviewing a pull request.

## Resource entry

- [ ] The resource is about physics or is directly used by physicists.
- [ ] It is open source, open access, free, or freemium.
- [ ] The URL points to the canonical project page and returns a 2xx status.
- [ ] The URL is stable (an official site, an archive, or a repository).
- [ ] The entry uses the standard list format:

  ```markdown
  - [Name](https://example.org/) - Description ending with a period. `[OS]` `[Free]`
  ```

- [ ] The description is one sentence, factual, and free of marketing language.
- [ ] The description starts with a capital letter and ends with a period.
- [ ] At least one label from `README.md#legend` is present.
- [ ] The entry sits in the most relevant section.

## Repository hygiene

- [ ] `make validate` passes.
- [ ] `make all` was run if entries or feeds changed.
- [ ] `dev/resources.json` is regenerated and committed.
- [ ] `dev/feeds.opml` is regenerated and committed when feeds change.
- [ ] No duplicate URLs were introduced.
- [ ] The table of contents still matches the section headings.
- [ ] Commit messages are clear and in the imperative mood.

## Licensing

- [ ] New prose is compatible with CC BY 4.0.
- [ ] New code carries an `SPDX-License-Identifier: GPL-3.0-or-later` header.
- [ ] No copyrighted text was copied verbatim without permission.
