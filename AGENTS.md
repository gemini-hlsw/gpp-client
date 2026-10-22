# gpp-client

Python client for GPP, whose GraphQL schema changes almost daily. Most of the client is generated from that schema.

## Read first

- Codegen and the generated-code check: `docs/source/developer/codegen.rst`.
- Schema updates: `docs/source/developer/schema.rst`.
- Releases: `docs/source/developer/releases.rst`.

## Commands

```bash
uv sync --locked --all-groups
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

## Rules

- Change GraphQL by editing `.graphql` files under `graphql/operations/` and rerunning codegen. `src/gpp_client/generated/` is output only.
- Commit regenerated code in the same change as the operation or schema change behind it.
- Tests run offline: mock GPP and REST calls.
