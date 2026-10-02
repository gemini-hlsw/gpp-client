# gpp-client architecture

How the code is put together today. Goals and policy live in [OVERVIEW.md](OVERVIEW.md); terms in [GLOSSARY.md](GLOSSARY.md).

## Layers

```
user code / gpp CLI
        |
GPPClient                     src/gpp_client/client.py
  |- domains                  src/gpp_client/domains/     hand-written
  |    |- generated client    src/gpp_client/generated/   ariadne-codegen output
  |    |- REST client         src/gpp_client/rest/        hand-written, aiohttp
  |- .graphql / .rest         direct access to the two clients
        |
ODB: /odb (GraphQL over HTTP), /ws (subscriptions), REST paths
```

- **`GPPClient`** resolves settings and builds one generated GraphQL client (httpx) and one REST client (aiohttp) against the same base URL. It passes both to each GPP domain. Everything is async.
- **Domains** (`client.program`, `client.observation`, `client.target`, `client.attachment`, `client.workflow_state`, `client.goats`, `client.scheduler`, `client.atom`, `client.site_status`) turn generated methods and REST calls into task-shaped methods. Most are thin. `scheduler` combines GraphQL with REST atom digests. `attachment` uses REST for file transfer. `site_status` scrapes gemini.edu, takes no clients, and does not touch GPP.
- **The CLI** (`gpp`, built on Typer, in `src/gpp_client/cli/`) is hand-written commands over the domains.
- **The public API** is `GPPClient` and `__version__` (`src/gpp_client/__init__.py`). Generated models are importable from `gpp_client.generated` for custom calls.

## Code generation

ariadne-codegen, a generator that turns a GraphQL schema plus operations into a typed Python client, produces everything in `src/gpp_client/generated/`. Nobody edits it by hand. ([ADR 0001](adr/0001-generated-code-committed.md))

```
GPP server --download_schema.py--> graphql/schemas/<env>.graphql
graphql/operations/**.graphql --run_codegen.py--> src/gpp_client/generated/
```

- **Schemas** are downloaded with `scripts/download_schema.py <ENV>`. It uses introspection (asking the server to describe its own schema), configured by `graphql/schemas/<env>.toml`.
- **Operations** are hand-written `.graphql` files grouped by domain under `graphql/operations/shared/domains/`. Operations that exist only on development go in `graphql/operations/development_only.graphql`, which must be additive: no name may collide with `shared/`.
- **Codegen** runs `scripts/run_codegen.py <ENV>`, configured by `graphql/codegen/<env>.toml`:
  1. It assembles `shared/`, plus `development_only.graphql` for development, into `build/`.
  2. It deletes and regenerates `src/gpp_client/generated/`.
  3. It writes `generated/package_environment.py`, recording which environment the code was built for.
- **Codegen validates operations.** It fails with `InvalidOperationForSchema` when an operation asks for something the schema lacks.
- **Plugin:** `src/custom_plugins/` holds one ariadne-codegen plugin. It wraps generated input-field aliases in `str()` so Pyright and VS Code type them correctly.
- **`convert_to_snake_case` must stay on.** The scheduler depends on it (comment in `graphql/codegen/*.toml`).

The step-by-step procedure is in [agents/schema-update.md](agents/schema-update.md).

## Environments and settings

- `GPPEnvironment` (`src/gpp_client/environment.py`) has `DEVELOPMENT` and `PRODUCTION`, with URLs in `src/gpp_client/constants.py`. There is no staging entry.
- The active environment comes from `generated/package_environment.py`, so the generated code and the default server are fixed when the package is built. ([ADR 0002](adr/0002-environment-fixed-at-build-time.md))
- `GPPSettings.environment_override` (env var `GPP_ENVIRONMENT_OVERRIDE`) changes the server at runtime. It is meant for tooling: the generated code still matches the build, so it can disagree with the server it now talks to.
- `GPPSettings` (`src/gpp_client/settings.py`, pydantic-settings, prefix `GPP_`) reads its sources in this order, highest priority first:
  1. constructor arguments
  2. environment variables
  3. `.env`
  4. the user's `config.toml` (path from `gpp get-config-path`)
  5. file secrets
- Tokens: `GPP_TOKEN` for production, `GPP_DEVELOPMENT_TOKEN` for development. `GPPClient(token=...)` fills whichever one the package's environment uses.

## Releases

- The `Create Release` workflow (`.github/workflows/create_release.yaml`, run by hand) takes a tag and:
  1. checks the tag with `scripts/validate_release.py`
  2. runs lint and tests
  3. builds the package and smoke-tests the wheel
  4. pushes the tag and drafts a GitHub release

  Publishing that draft triggers `publish.yaml`, which uploads to PyPI.
- `validate_release.py` requires the committed generated code to match the tag:

  | Tag | Required generated code |
  |---|---|
  | `vYY.M.PATCH.devN` | `DEVELOPMENT` |
  | `vYY.M.PATCH` | `PRODUCTION` |

- Git history shows `main` carrying development code between releases (656c2c3 switched to production for 26.9.0; d37b443 switched back).
- Docs build on ReadTheDocs from `docs/source/` (Sphinx).

## Tests

- `tests/` mirrors `src/`. It uses pytest with pytest-asyncio and xdist, and every test mocks the network.
- `run_tests.yaml` runs ruff and pytest on pull requests and pushes to `main`. Pushes run Python 3.11 to 3.14.
- `check_codegen.yaml` runs both codegen targets on pushes to `main`, and on pull requests that change GraphQL or codegen inputs.

The target testing policy is in [OVERVIEW.md](OVERVIEW.md#testing-policy).
