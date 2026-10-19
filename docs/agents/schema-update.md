# Schema update

How to bring the client up to date with GPP. Read [ARCHITECTURE.md](../ARCHITECTURE.md#code-generation) first if codegen is new to you.

One build generates the client from the merged schema of both environments, development and production, plus a trimmed copy of every operation per environment. Nothing is sorted by environment by hand.

## Routine update

1. Run the update:
   ```bash
   uv run --group codegen python -m scripts.schema_update
   ```
   It introspects both environments, writes each changed schema to `src/gpp_client/schemas/<environment>.graphql` with a `# schema-date:` first line, rebuilds the generated client, and runs `pytest`. Running it twice without a GPP change is a no-op. No token is needed. If a server refuses anonymous introspection, the command names the token variable to set (`GPP_DEVELOPMENT_TOKEN` or `GPP_TOKEN`); a maintainer sets it in their own terminal.
2. When an environment answers with a schema that does not build, the command keeps that environment's committed schema, updates the other, and names the held environment in its output. That is a problem in GPP, not the client: run the update again later, and pass the name to `release_notes --held` at the next release.
3. The build fails, naming what to fix, when:
   - an operation selects something no environment has (`Operations select what no environment has`, listing each): fix the operation under `graphql/operations/`;
   - a trimmed copy is invalid on its environment (`Trimmed operations are invalid`), for example a variable declared nullable where that environment requires it: change the operation, the build never retypes a variable;
   - codegen fails on another GraphQL rule: the message says which.

   A difference between the environments never fails the build. A field whose type differs takes production's type; a type name of a different kind on each environment takes production's definition, dropping development-only uses; production's old name for a renamed input type or enum becomes an alias. All of it is listed in the merge summary.
4. Read `git diff src/gpp_client/schemas/`. Note removed or renamed fields and types: those break operations and belong in the PR description.
5. The build prints ariadne-codegen's deprecation warnings: each names a deprecated field that an operation selects, or a deprecated input field the generated input types carry. Note new ones in the PR description.
6. The command ends with three Markdown summaries, which go into the PR body: the schema update summary (per environment: changed, unchanged or held), the merge summary (`Renamed`, `Alias ... of ... in ...`, `Warning` for a renamed union or interface, `Conflict`, `Kind conflict`, `Ambiguous`, `Collision` lines) and the trim summary (per environment, the unavailable operations and each part removed from which operations and fragments).
7. Run `uv run ruff check . && uv run ruff format --check .` and `uv run ty check --error-on-warning src/gpp_client`. Fix domains whose generated method or model names changed. A failing test in `tests/docs/` names a docs example that uses a changed name.
8. Done when the checks pass and the schemas, operations and `src/gpp_client/generated/` changes are in one PR.

## Release prep

A release is a tag on `main`. Every release reaches every environment in one stream. Releases are manual; the full procedure is `docs/source/developer/releases.rst`.

1. Check the release locally before asking the user to run the `Create Release` workflow. The check wants the tag on the commit and the package reinstalled from it, so tag locally, check, and delete the tag again:
   ```bash
   git tag v26.5.0
   uv run --group codegen python -m scripts.validate_release v26.5.0
   git tag -d v26.5.0
   ```
   It refuses a tag that is not `vYY.M.PATCH`, a baked `src/gpp_client/_version.py` that differs from the tag, and a checkout whose `src/gpp_client/generated/` differs from a fresh build. On a mismatch, run the schema update, commit the result in its own PR, and check again.
2. Preview the release notes, naming a held environment if the schema update held one:
   ```bash
   uv run --group codegen python -m scripts.release_notes v26.4.0 [--held development]
   ```
   The script compares each environment's committed schema at the previous tag with the working copy and prints Markdown: a `Production: changed/unchanged` and `Development: changed/unchanged` headline, then per changed environment a `Breaking` list (graphql-core's `find_breaking_changes`) and an `Added or relaxed` list (`find_dangerous_changes`), the aliases this release adds, a dropped alias under production's `Breaking`, and the held environment with the commit its schema is from.
3. The user runs `Create Release` with the tag and, if any, the held environment. It tags locally, validates, runs lint and tests, drafts a release whose notes start with the output of `release_notes` against the nearest earlier `v*` tag, followed by GitHub's generated notes; when there is no previous tag, or it has no committed schemas, the draft has only GitHub's notes.
4. The user publishes the draft. Publishing runs `Upload Python Package`, which uploads to PyPI.
