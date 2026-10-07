# gpp-client architecture

How the code is put together. Goals and policy live in [OVERVIEW.md](OVERVIEW.md); terms in [GLOSSARY.md](GLOSSARY.md).

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

- **`GPPClient`** resolves settings, including the environment, and builds one generated GraphQL client (httpx) and one REST client (aiohttp) against that environment's base URL. It passes both to each GPP domain. Everything is async. A caller can pass its own `httpx.AsyncClient` as `http_client`; `GPPClient` sends every GraphQL HTTP request through it, adding the auth header per request without changing the caller's client.
- **Domains** (`client.program`, `client.observation`, `client.target`, `client.attachment`, `client.workflow_state`, `client.goats`, `client.scheduler`, `client.atom`, `client.site_status`) turn generated methods and REST calls into task-shaped methods. Most are thin. `scheduler` combines GraphQL with REST atom digests. `attachment` uses REST for file transfer. `site_status` scrapes gemini.edu, takes no clients, and does not touch GPP.
- **The CLI** (`gpp`, built on Typer, in `src/gpp_client/cli/`) is hand-written commands over the domains.
- **The public API** is `GPPClient` and `__version__` (`src/gpp_client/__init__.py`). Generated models are importable from `gpp_client.generated` for custom calls.

## Code generation

ariadne-codegen, a generator that turns a GraphQL schema plus operations into a typed Python client, produces everything in `src/gpp_client/generated/`. Nobody edits it by hand. ([ADR 0001](adr/0001-generated-code-committed.md))

```
GPP servers --download_schema--> graphql/schemas/<env>.graphql (development, production)
graphql/schemas/<env>.graphql + graphql/operations/**.graphql --build_client-->
    graphql/schemas/merged.graphql
    src/gpp_client/generated/                     (one ariadne-codegen run on the merged schema)
    src/gpp_client/generated/trimmed/<env>.py     (each operation trimmed per environment)
    src/gpp_client/generated/environment_clients.py (typed views of the client per environment)
    src/gpp_client/generated/schemas/<env>.graphql (development and production schemas, without descriptions)
    llms.txt                                      (usage and availability notes for AI agents)
```

- **Schemas** are downloaded with `python -m scripts.download_schema`, which fetches both environments by introspection (asking the server to describe its own schema). It asks anonymously, and uses an environment's token (`GPP_DEVELOPMENT_TOKEN`, `GPP_TOKEN`) only when that server refuses. It keeps `@oneOf`, `@specifiedBy` and deprecated input values.
- **The build** is `python -m scripts.build_client`, whose `build()` is the pipeline's one entry point. It merges the schemas, runs codegen once, trims every operation per environment, and prints a trim summary.
- **The merged schema** (`scripts/schema_merge.py`) is committed as `graphql/schemas/merged.graphql`. Every type, field, argument, input field and enum value not on both environments carries `@environments(names: [...])`. Conflict rules ([ADR 0006](adr/0006-merged-schema-runtime-environment.md)):
  - differing output nullability becomes nullable;
  - differing input or argument nullability becomes optional;
  - a part on only some of the environments that have its parent becomes nullable (output) or optional (input);
  - a field or input field whose type differs is left out, and so is a field with an argument whose type differs; the build warns, and fails if an operation selects such a field, naming it and each environment's type;
  - a type of a different kind fails the build.

  Descriptions and defaults come from the newest environment that has the part.
- **Operations** are hand-written `.graphql` files grouped by domain under `graphql/operations/domains/`. Every operation is written once, against the merged schema; nothing is sorted by environment.
- **Codegen** is one ariadne-codegen run on the merged schema, configured by `graphql/codegen.toml`; the build fills in the paths. It deletes and regenerates `src/gpp_client/generated/`.
- **Codegen validates operations** against the merged schema, so a field that exists on no environment still fails the build.
- **Trimmed operations** (`scripts/trim_operations.py`): for each environment, each operation as the generated client embeds it loses the fields, arguments, inline fragments and fragment spreads that environment lacks; unused variables and fragments go too, and a selection left empty gets `__typename`. An operation whose root field the environment lacks is stored as unavailable. Each copy is validated against that environment's schema, and any failure fails the build. `generated/trimmed/__init__.py` lists every generated operation in `GENERATED`, keyed by a whitespace-insensitive digest of the embedded query. `generated/trimmed/<env>.py` stores a copy only for an operation the environment receives differently: `OPERATIONS` (name, trimmed text or `None` when unavailable, fragment names) and the `FRAGMENTS` those use, each once. `gpp_client.trimmed_operations.find_trimmed_operation(environment, query)` returns what to send: the stored copy, the generated query unchanged when none is stored, or `document=None` when unavailable; a query-builder call returns `None`, even when it reuses a generated operation name. The build reads every query back from the generated client source and fails, naming the operation, if the lookup misses one on any environment. The runtime sends what it returns, and the generated query when it returns `None`. Over HTTP and websocket, `document=None` raises `GPPEnvironmentError` before sending.
- **Typed views** (`generated/environment_clients.py`): the build writes `SharedGraphQLClient` (the generated client methods on both development and production), and `DevelopmentGraphQLClient` and `ProductionGraphQLClient` on top of it, each adding the methods only its environment has. A method's environments come from the trimmed operations: a method whose operation is unavailable on an environment is left out of that environment's view. Each view assigns the generated method itself, so editors show its signature and docstring. `EveryEnvironmentGraphQLClient` inherits every view, so the full client is typed as each one.
- **Availability for `llms.txt`** (`scripts/availability.py`): the build reads the merged schema's `@environments` directives into three lists: each environment-specific argument (`Type.field(arg:)`), input field (`Input.field`) and enum value (`Enum.VALUE`) with the environments that have it; each input field the merged schema makes optional (conflict rules 2 and 3) with the environments that require it, read from each environment's schema; and, per operation, each field it selects (`Type.field`, fragments included) that development lacks, with the environments that still have it. Promotion is linear, so those fields leave next. Nothing in them is hand-listed.
- **Bundled schemas:** the build copies the development and production schemas, without descriptions (about 165 KB each, 30 KB compressed in the wheel), into `generated/schemas/`, for the checks before sending.
- **`llms.txt`** (`scripts/llms_txt.py`): the build writes it at the repo root: fixed text on choosing the environment, errors and warnings, then an availability section listing, for development and production, the client methods, arguments, input fields and enum values only that environment has, input fields only it requires, the selected fields that read `None` on it, and the fields leaving production. The lists come from the trimmed operations and `scripts/availability.py`. Sphinx serves it at the docs root (`html_extra_path`).
- **Diffs:** `.gitattributes` marks `src/gpp_client/generated/`, `graphql/schemas/*.graphql` and `llms.txt` as `linguist-generated`, so GitHub collapses them in PR diffs.
- **Trim summary:** the build prints, per environment, the unavailable operations and each removed part with the operations and fragments it left, as Markdown for the schema-update PR body.
- **Plugins:** `src/custom_plugins/` holds the ariadne-codegen plugins, registered in `graphql/codegen.toml`:
  - `AliasStrWrapperPlugin` wraps generated input-field aliases in `str()` so Pyright and VS Code type them correctly.
  - `TolerantEnumsPlugin` bases every generated enum on `_TolerantEnum`, so an enum value GPP adds after the build parses as a member carrying the raw value instead of failing validation. Repeated unknown values return the same member.
  - `CaptureOperationsPlugin` hands the build each operation string exactly as the generated client embeds it, so the trimmed copies start from the same text.
  - `EnvironmentDefaultsPlugin` gives a result field the default `None` only when it is on fewer environments than its parent type, since an environment that lacks it sends no key. Every other field stays required. The build reads the generated models back and fails, naming each field, if an environment-specific selection did not get that default.
  - `AvailabilityDocstringsPlugin` starts the docstring of each environment-specific client method, result field, input type, input field, enum and enum value with `Available on: <environments>.`, ahead of any schema description. It names development and production only, and marks nothing that is on both. A method's environments are those that have every root field its operation selects; a field or value is marked only when it is on fewer environments than its parent type. `ClientForwardRefsPlugin`, which `lazy_imports` would otherwise append last, is listed before it in `codegen.toml` so the import it puts at the top of each method does not push the docstring down.
- **`convert_to_snake_case` must stay on.** The scheduler depends on it (comment in `graphql/codegen.toml`).
- **`lazy_imports` is on**, so `gpp_client.generated` loads a module only when a name from it is used. Domains keep it that way: they import generated models under `TYPE_CHECKING`, or inside the method that builds one. A top-level import of `input_types` adds about 0.3 s to `import gpp_client.client`, more than the import itself.

The step-by-step procedure is in [agents/schema-update.md](agents/schema-update.md).

## Environments and settings

- `GPPEnvironment` (`src/gpp_client/environment.py`) has `DEVELOPMENT` and `PRODUCTION`, in promotion order. Its one table gives each its base URL and token variable; settings, the CLI choices, the download script and the build derive their lists from it. Only the `GPPClient.__init__` overloads are hand-written, since type checkers need literals; a test checks them against the table.
- The environment is chosen when a `GPPClient` is built, in this order: `GPPClient(environment=...)`, `GPP_ENVIRONMENT`, `.env`, `environment` in `config.toml`, then production. Names ignore case and surrounding spaces. An empty value falls through to the next source; an unknown name raises `GPPClientError` listing the valid names. ([ADR 0006](adr/0006-merged-schema-runtime-environment.md))
- `GPPGraphQLClient` (`src/gpp_client/graphql_client.py`) is the generated client plus `EnvironmentGraphQLClient`, which sends the auth headers with every HTTP request and replaces each generated operation, over HTTP and websocket, with the selected environment's trimmed copy from `find_trimmed_operation`. So a field the environment lacks is never requested and reads `None`. Each client holds its own environment, so clients on different environments work side by side in one process.
- `GPPGraphQLClient` also inherits every typed view, through `EveryEnvironmentGraphQLClient`. `GPPClient` is generic over the type of `client.graphql`: `@overload`s on `__init__` type a client built with `environment="development"` or `"production"` (or the `GPPEnvironment` member) with that environment's view, so a type checker flags an operation the environment lacks. Any other client, such as one whose environment comes from settings, is typed with the full `GPPGraphQLClient`. A bare `GPPClient` annotation means `GPPClient[SharedGraphQLClient]`, so it accepts a client on either environment. The runtime object is always the full client; the views only change what type checkers see.
- Before an HTTP request or a websocket subscription, `EnvironmentGraphQLClient` checks the call against the selected environment. A generated operation the environment lacks raises `GPPEnvironmentError` (`src/gpp_client/exceptions.py`) with `kind` `EnvironmentItemKind.OPERATION`. Every other call goes through `check_document` (`src/gpp_client/document_checks.py`): a generated operation as each environment receives it, its trimmed copy, and a query-builder call (`client.graphql.query(...)`, `mutation(...)`) or raw `execute` as written. It validates the document with graphql-core, and coerces its variables as sent, against each environment's schema from `generated/schemas/<env>.graphql`; a set variable whose argument an environment's trimmed copy dropped fails that environment. When the selected environment fails, the error names the first field, argument, input field or enum value it lacks, or the first argument or input field it requires. `available` holds the environments that accept the call; when none does, as when a call sets both a field and its replacement, it holds the environments that have the item, or may leave it unset. When no environment has the item, as with a misspelled field, the call is sent unchanged and GPP reports the mistake. The error also names its kind (`EnvironmentItemKind`, a `StrEnum` whose values read as they do in the message) and the selected environment, and says what to change. Environments travel as `GPPEnvironment`; `GPPEnvironment.label` is the lowercase name the generated package and messages use. Variables the trimmed copy does not declare are left out of the request.
- When the check passes on production, `warn_leaving_field` (`src/gpp_client/leaving_fields.py`) emits `GPPFieldLeavingWarning`, a `FutureWarning`, for each selected field development lacks, once per field per process. A subscription raises or warns when iterated, before it connects. Each schema is built on first use (about 90 ms each; production's first call loads development's too, for the leaving check); validation is cached per document, so a repeated document costs microseconds and a new one under a millisecond.
- `RESTClient` (`src/gpp_client/rest/client.py`) knows its environment. When a scheduler REST path answers 404, it raises `GPPEnvironmentError` with `kind` `EnvironmentItemKind.REST_PATH`, naming the path and the environment, with `available` empty. That 404 arrives after sending, and nothing tells which environment serves the path, so the message names no other environment and does not say nothing was sent. Attachment REST calls in `domains/attachment.py` keep raising `GPPResponseError` on 404, which there means a missing attachment.
- The client logs one INFO line at start naming the environment and its GraphQL URL.
- The CLI (`src/gpp_client/cli/`, Typer) builds every client through `open_client()` in `cli/utils.py`, which passes the global `gpp --env` choice as `environment=` and prints `Environment: <name> (<url>)` to stderr. `--env` and `gpp set-default-env` offer development and production only. `set-default-env` writes `environment` into `config.toml` through `settings.set_default_environment`, creating the file if missing, editing only that top-level line, and refusing to write when the result would not parse to the old settings plus the new environment.
- `GPPSettings` (`src/gpp_client/settings.py`, pydantic-settings, prefix `GPP_`) reads its sources in this order, highest priority first:
  1. constructor arguments
  2. environment variables
  3. `.env`
  4. the user's `config.toml` (path from `gpp get-config-path`)
  5. file secrets
- Tokens: `GPP_TOKEN` for production, `GPP_DEVELOPMENT_TOKEN` for development. `GPPClient(token=...)` fills the selected environment's slot. A missing token raises `GPPAuthError` naming the variable to set.

## Releases

- The `Create Release` workflow (`.github/workflows/create_release.yaml`, run by hand) takes a tag and:
  1. validates the release with `python -m scripts.validate_release <tag>`
  2. runs lint and tests
  3. builds the package and smoke-tests the wheel
  4. pushes the tag and drafts a GitHub release

  `python -m scripts.release_notes <previous tag>` (`scripts/release_notes.py`) diffs `graphql/schemas/merged.graphql` at that tag against the working copy and prints, per development and production, the parts new to it and removed from it, and the parts newly leaving production. A part whose parent changed the same way is not listed separately. The maintainer pastes it into the draft.

  Publishing that draft triggers `publish.yaml`, which uploads to PyPI.
- Releases are one stream: every release reaches every environment. `validate_release` refuses:
  - a tag that is not `vYY.M.PATCH`; a `.devN` tag gets a message explaining the single stream;
  - a checkout whose `graphql/schemas/merged.graphql`, `src/gpp_client/generated/` or `llms.txt` differs from a fresh build of the committed schemas and operations. It builds into a temporary folder, so the checkout is never changed.
- Docs build on ReadTheDocs from `docs/source/` (Sphinx).

## Tests

- `tests/` mirrors `src/`. It uses pytest with pytest-asyncio and xdist, and every test mocks the network.
- The runtime finds the generated package through `gpp_client.generated_tables`: `load_generated` for the trimmed tables and `generated_package` for the bundled schemas. Tests of environment behavior build a small client from fixture schemas with `build_fixture` (`tests/gpp_client/fixture_build.py`) and read its tables inside its `tables()` context, which wraps `use_generated_package`. They never rely on what is environment-specific in the committed schemas, since a schema update changes that whenever GPP promotes something; `GPPClient`-seam tests call the fixture's generated methods or query builder on a real `GPPClient`.
- Runtime tests build a real `GPPClient` with the `gpp_client` and `gpp_transport` fixtures in `tests/gpp_client/conftest.py`: an httpx `MockTransport` that returns canned GraphQL responses and records each request. `test_workflow_state.py::test_get_by_id_sends_query_and_returns_model` is the pattern.
- `tests/gpp_client/client/test_every_operation.py` runs every generated operation on every environment. Its fake GPP validates the document the client sent against that environment's committed schema, then answers with a response built from that schema, once with every nullable field null and once with every field filled; the client must parse both. It asserts nothing environment-specific, so it passes on any committed schemas. Custom scalars are typed `Any` in the generated models, so a null where a model requires a custom scalar still parses; see [Known gaps](OVERVIEW.md#known-gaps).
- Subscriptions run against `SubscriptionServer` (`tests/gpp_client/subscription_server.py`), a local `websockets` server speaking graphql-transport-ws, and REST against a local aiohttp server; `tests/gpp_client/domains/test_scheduler_environments.py` points a client's `graphql.ws_url` and `rest.base_url` at them.
- `run_tests.yaml` runs ruff, ty (Astral's type checker, a dev dependency) on `src/gpp_client`, and pytest on pull requests and pushes to `main`. ty fails on warnings too; `pyproject.toml` relaxes three of its rules for `generated/async_base_client.py`, which ariadne-codegen copies verbatim. Pushes run Python 3.11 to 3.14.
- `pre_commit.yaml` runs every hook in `.pre-commit-config.yaml` on the files a pull request or push changes, skipping `no-commit-to-branch`, which only guards local commits.
- `tests/scripts/test_environment_typing.py` builds a client from fixture schemas into a copy of `gpp_client`, runs ty on small files that use it, and compares the lines ty flags with the lines marked `# error`.
- `check_schema.yaml`, run by hand, downloads each environment's schema anonymously and fails when it differs from the committed file.
- `check_codegen.yaml` runs the build on every pull request and push to `main`, and fails when the committed `graphql/`, `generated/` or `llms.txt` files differ from the build.
- `check_environment_independence.yaml` runs `python -m scripts.check_environment_independence` on pull requests and pushes to `main`. The script copies the checkout to a scratch directory, copies the development schema over production there, rebuilds and runs pytest, so a test that reads environment differences from the committed schemas fails. Run it locally the same way.

The target testing policy is in [OVERVIEW.md](OVERVIEW.md#testing-policy).
