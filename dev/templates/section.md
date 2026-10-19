# Section Template

Use this template when proposing a new section.

1. Add a bullet to the table of contents in `README.md`, keeping the anchor that
   GitHub generates: lowercase, spaces replaced by dashes, punctuation removed.

   ```markdown
   - [Section Name](#section-name)
   ```

2. Add the heading and at least three entries in the body:

   ```markdown
   ## Section Name

   - [Resource One](https://example.org/) - Description. `[OS]` `[Free]`
   - [Resource Two](https://example.org/) - Description. `[OA]` `[CC]`
   - [Resource Three](https://example.org/) - Description. `[Freemium]`
   ```

3. Regenerate the derived files:

   ```sh
   make all
   ```

4. Explain in the pull request why the section does not fit an existing one.
