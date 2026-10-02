# Schema update

How to bring the client up to date with GPP. Read [ARCHITECTURE.md](../ARCHITECTURE.md#code-generation) first if codegen is new to you.

The generated client holds code for one environment at a time, and the last `run_codegen.py` run wins. Between releases `main` holds development code, so finish every routine update with a DEVELOPMENT codegen run. Check which one is committed in `src/gpp_client/generated/package_environment.py`.

## Routine update (between releases)

1. Set `GPP_DEVELOPMENT_TOKEN` and `GPP_TOKEN`. The download script exits without them.
2. Download both schemas:
   ```bash
   uv run --group schema python scripts/download_schema.py DEVELOPMENT
   uv run --group schema python scripts/download_schema.py PRODUCTION
   ```
3. Read `git diff graphql/schemas/`. Note removed or renamed fields and types: those break operations and belong in the PR description.
4. Check the operations still build against production, then regenerate for development:
   ```bash
   uv run --group codegen python scripts/run_codegen.py PRODUCTION
   uv run --group codegen python scripts/run_codegen.py DEVELOPMENT
   ```
   When codegen fails on a removed field, fix the operation under `graphql/operations/` and rerun. An operation that now works only on development moves to `development_only.graphql`.
5. Run `uv run pytest` and `uv run ruff check .`. Fix domains whose generated method or model names changed.
6. Done when `package_environment.py` says `DEVELOPMENT`, tests pass, and the schemas, operations and `generated/` changes are in one PR.

## Release prep (before a production release)

1. Download the production schema as in step 2 above.
2. Move every operation and fragment in `development_only.graphql` that production now supports into `shared/`. Leave the rest.
3. Run `run_codegen.py PRODUCTION` last, then the tests. Merge this as its own PR.
4. Run the `Create Release` workflow with tag `vYY.M.PATCH`. It refuses the tag unless the committed code is PRODUCTION.
5. After the release, regenerate for DEVELOPMENT in a follow-up PR.

A pre-release (`vYY.M.PATCH.devN`) needs DEVELOPMENT code, which `main` already holds between releases.
