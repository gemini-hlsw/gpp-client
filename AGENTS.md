# gpp-client

Python client for GPP, whose GraphQL schema changes almost daily. Most of the client is generated from that schema.

## Read first

- Direction, goals, users, principles, release contract, testing policy, known gaps: `docs/OVERVIEW.md`.
- Code changes - layers, codegen, environments, releases: `docs/ARCHITECTURE.md`.
- Codegen, schema updates, release prep: follow `docs/agents/schema-update.md`.
- Terms and past decisions: `docs/agents/domain.md` (glossary and ADRs).
- Judgement rules for writing and reviewing code: `docs/source/developer/coding-standards.rst`.

## Commands

```bash
uv sync --locked --all-groups
uv run pytest
uv run ruff check . && uv run ruff format --check .
uv run ty check --error-on-warning src/gpp_client
```

- Before the first commit in a clone, run `pre-commit install` (getting the tool: `docs/source/developer/setup.rst`). Worktrees share the clone's hooks.
- Every commit passes the hooks. When a hook fixes files, stage them and commit again; never `--no-verify`.

## Rules

- Change GraphQL by editing `.graphql` files under `graphql/operations/` and rerunning codegen. `src/gpp_client/generated/` is output only.
- Commit regenerated code in the same change as the operation or schema change behind it.
- Tests run offline: mock GPP and REST calls.
