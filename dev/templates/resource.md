# Resource Entry Template

Copy this into the most relevant section of `README.md`.

```markdown
- [Resource Name](https://example.org/) - One factual sentence describing what the resource is and who it is for. `[OS]` `[Free]`
```

Rules:

- The link text is the name of the resource.
- The URL is the canonical, stable address, preferably `https://`.
- The description is a single sentence ending with a period.
- Tags come from `README.md#legend` and are wrapped in backticks.

If the resource also provides a feed, add a row to `dev/data/feeds.csv`:

```csv
Resource Name,https://example.org/feed.xml,https://example.org/,Physics
```
