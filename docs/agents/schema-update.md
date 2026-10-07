# Schema update

How to bring the client up to date with GPP. Read [ARCHITECTURE.md](../ARCHITECTURE.md#code-generation) first if codegen is new to you.

One build generates the client from the merged schema of both environments, development and production, plus a trimmed copy of every operation per environment. Nothing is sorted by environment by hand.

## Routine update

1. Download both schemas, then build:
   ```bash
   uv run --group schema python -m scripts.download_schema
   uv run --group codegen python -m scripts.build_client
   ```
   No token is needed. If a server refuses anonymous introspection, the download names the token variable to set (`GPP_DEVELOPMENT_TOKEN` or `GPP_TOKEN`); a maintainer sets it in their own terminal.
2. The build fails, naming what to fix, when:
   - a type is a different kind on two environments: report it upstream;
   - an operation selects a field whose type differs between environments: the message names the field and each environment's type; change the operation or wait for promotion;
   - an operation selects something no environment has: fix the operation under `graphql/operations/`;
   - a trimmed copy is invalid on its environment, for example an input-object literal field that environment lacks: the message names the operation and environment; pass the value as a variable or change the operation.

   It warns about each field whose type differs but no operation selects; that field is left out of `merged.graphql`, so note it in the PR description.
3. Read `git diff graphql/schemas/`. Note removed or renamed fields and types: those break operations and belong in the PR description. In `merged.graphql`, `@environments(names: [...])` markers that appear or disappear show what moved between environments.
4. The build prints ariadne-codegen's deprecation warnings: each names a deprecated field that an operation selects, or a deprecated input field the generated input types carry. Note new ones in the PR description.
5. The build ends with a Markdown trim summary: per environment, the operations it lacks and each part removed from which operations and fragments. Paste it into the PR body.
6. Run `uv run ruff check . && uv run ruff format --check .`, `uv run ty check --error-on-warning src/gpp_client`, `uv run pytest` and `uv run python -m scripts.check_environment_independence`. Fix domains whose generated method or model names changed.
7. Done when tests pass and the schemas (including `merged.graphql`), operations and `generated/` changes are in one PR.

## Release prep

A release is a tag on `main`. Every release reaches every environment in one stream.

1. Check the release locally before asking the user to run the `Create Release` workflow:
   ```bash
   uv run --group codegen python -m scripts.validate_release v26.5.0
   ```
   It refuses a tag that is not `vYY.M.PATCH`, and a checkout whose `merged.graphql`, `generated/` or `llms.txt` differs from a fresh build. On a mismatch, run the build, commit the result in its own PR, and check again.
2. The user runs `Create Release` with the tag. It creates a draft release with GitHub's generated notes.
3. List what the release changes per environment, from the previous release tag:
   ```bash
   uv run --group codegen python -m scripts.release_notes v26.4.0
   ```
   It compares `merged.graphql` at that tag with the working copy and prints Markdown: per development and production, the parts new to it and the parts removed from it, and the parts leaving production (gone from development, still on production). Paste it at the top of the draft's notes. If the tag has no `merged.graphql`, the script says so and stops.
4. The user publishes the draft. Publishing runs `Upload Python Package`, which uploads to PyPI.
