# Maintaining Awesome Physics

Routine tasks for maintainers.

## Weekly

- Review new issues and pull requests.
- Let the [link check workflow](../.github/workflows/link-check.yml) run and fix
  any newly broken links. The workflow runs every Monday.
- Merge or close stale pull requests.

## Monthly

- Run `make links` locally and triage warnings.
- Remove resources that are abandoned, paywalled, or no longer maintained.
- Check that the "Related Awesome Lists" section still points to live projects.

## When merging a pull request

1. Confirm the entry format and labels.
2. Confirm the entry exists in every translation (`README.md` and
   `README.pt-BR.md`) in the same section and order.
3. Confirm `make validate` passes on the branch.
4. Confirm generated artifacts are committed (`dev/resources.json`,
   `dev/resources.pt-BR.json`, and `docs/`).
5. Squash-merge with a clear message in the imperative mood.
6. Optionally run `make all && make site` if the contributor forgot.

## When a link breaks

1. Try to find the successor project or a stable archive.
2. If the resource still exists under a new URL, update the URL.
3. If it is gone, remove the entry and note it in the pull request.
4. If it is temporarily down, leave it and re-check on the next run.

## Branches

- `main` — stable, released content. GitHub Pages publishes from `main` / `docs`.
- `develop` — integration branch for the next release. Day-to-day work, new
  resources, and translation updates land here first.
- `release/X.Y` — maintenance branches for a released line (for example
  `release/1.0`). Only link fixes and translation syncs go here.

Merge `develop` into `main` when preparing a release. Do not commit directly to
a `release/*` branch.

## Releases and archival

The list uses [Semantic Versioning](https://semver.org/) with annotated tags
named `vMAJOR.MINOR.PATCH`:

- **MAJOR** — a change that affects every user, such as a new license or a
  restructured list.
- **MINOR** — new sections, a new language, or a large batch of resources.
- **PATCH** — fixed links, corrected descriptions, or small additions.

Release checklist:

1. Confirm `make all && make validate` passes for both languages.
2. Confirm generated artifacts are committed (`dev/resources*.json`, `docs/`).
3. Merge `develop` into `main` and push.
4. Write bilingual release notes (English and Portuguese).
5. Create an annotated tag:
   `git tag -a vX.Y.Z -m "Awesome Physics vX.Y.Z"`.
6. Push the tag and publish the release:
   `git push origin vX.Y.Z` and
   `gh release create vX.Y.Z --verify-tag --title "vX.Y.Z" --notes-file notes.md`.
7. Fast-forward `develop` to the release commit.

Archiving a release to [Zenodo](https://zenodo.org/) mints a DOI, which makes
the list citable. Connect the repository to Zenodo and publish a release there.

Keep the `NOTICE` file and license texts up to date.

## Adding a new maintainer

- Active contributors with several merged pull requests can be invited.
- Update any maintainer list and grant triage permissions.
