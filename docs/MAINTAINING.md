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

## Releases and archival

- Tag significant milestones (for example `v2026.10`).
- Archiving a release to [Zenodo](https://zenodo.org/) mints a DOI, which makes
  the list citable. Connect the repository to Zenodo and publish a release.
- Keep the `NOTICE` file and license texts up to date.

## Adding a new maintainer

- Active contributors with several merged pull requests can be invited.
- Update any maintainer list and grant triage permissions.
