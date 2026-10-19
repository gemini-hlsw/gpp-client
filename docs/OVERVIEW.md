# gpp-client overview

What gpp-client is for, who depends on it, and the rules we hold it to. How the code is built lives in [ARCHITECTURE.md](ARCHITECTURE.md); terms are defined in [GLOSSARY.md](GLOSSARY.md); the reasoning behind each decision is in [adr/](adr/).

## Purpose

gpp-client is the Python client for GPP, the Gemini Program Platform. GPP's API changes constantly, and gpp-client absorbs that churn so its users don't have to: they get typed models, domain methods (`client.program.get_by_id(...)`), and a `gpp` CLI instead of hand-writing GraphQL against a moving schema.

## Users

Many teams rely on it, at every level of Python experience:

- **GOATS**, which has its own domain (`client.goats`).
- **The scheduler team**, which has its own domain (`client.scheduler`), mixing GraphQL, REST and subscriptions.
- **Scientists and engineers** scripting against GPP, from notebooks to automation.
- **AI agents** writing code on behalf of any of the above. They are first-class users: the library should be easy for an agent to use correctly.

## Principles

In priority order. When two conflict, the higher one wins.

1. **Generated first, and complete.** Every part of the GPP API we support reaches users through the generated client. Coverage gaps are bugs. ([ADR 0004](adr/0004-generated-first-curated-on-top.md))
2. **Curated on top, and tested.** Curated conveniences sit on top of generated coverage, never in place of it, and each has a test that fails when the schema under it changes. ([ADR 0004](adr/0004-generated-first-curated-on-top.md))
3. **Easy to use and easy to maintain.** Both are the goal, and auto-generation is how we get both at once.
4. **Development and production from one install.** Users switch between them easily. See [Environments](#environments).

## How GPP changes

The GPP team owns the API. The server is the lucuma ODB:

https://github.com/gemini-hlsw/lucuma-odb

Its schema is one checked-in file:

https://github.com/gemini-hlsw/lucuma-odb/blob/main/modules/schema/src/main/resources/lucuma/odb/graphql/OdbSchema.graphql

| Environment | How it deploys | How often (Aug-Oct 2026) |
|---|---|---|
| development | automatically, on every push to their `main` | several times a day |
| staging | promoted by hand from development | about weekly |
| production | promoted by hand from staging | every two to three weeks |

The client tracks development and production only, so a change reaches it twice: on development, and later on production.

There is no announcement channel. The schema update command introspects both environments when a maintainer or an agent runs it, and `check_schema.yaml` compares the live schemas with the committed ones when started by hand.

## Data sources

| Source | What we use it for | Reached through |
|---|---|---|
| ODB GraphQL (`/odb`) | Programs, observations, targets, attachment metadata, workflow state, GOATS and scheduler queries | Generated client |
| ODB GraphQL subscriptions (`/ws`) | Live edits to programs, observations and targets; scheduler calculation updates | Generated client |
| ODB REST | Scheduler atom digests and visibility changes; attachment upload and download | `gpp_client.rest` |
| gemini.edu status pages | Site and instrument status (`client.site_status`) | HTML/JSON scraping, not GPP |

## Release contract

Releases are one stream. A release matches each environment's schema on its release date. A release is not guaranteed to work against GPP weeks later. Users should upgrade often.

When GPP removes or renames something, the break reaches users on their next upgrade. We keep no shims (adapters that keep old names working); release notes name what changed. ([ADR 0005](adr/0005-schema-breaks-pass-through.md)) The one exception is production's name for an input type or enum that development has renamed: it is a deprecated alias of the development-named class in exactly the releases whose pairing contains the rename, and it is dropped, under "Breaking", in the first release after the promotion. Type checkers resolve the alias but do not flag it; the release notes are the signal. ([ADR 0006](adr/0006-merged-schema-runtime-environment.md))

Release notes are generated per environment from the schema diff since the previous tag: "Production: changed/unchanged" and "Development: changed/unchanged" headlines, a "Breaking" and an "Added or relaxed" list per changed environment, the aliases, and any held environment. Releases are made by hand; see [Known gaps](#known-gaps).

Versions are CalVer (calendar versioning, `YY.M.PATCH`, such as `26.9.0`), set from the git tag. ([ADR 0003](adr/0003-calver-from-git-tags.md))

## Environments

The client reaches two GPP environments: development and production.

- **How it works:** one install reaches development and production. One generated client is built from the merged schema, and the environment is chosen at runtime: `GPPClient(environment=...)`, then `GPP_ENVIRONMENT`, then `.env`, then production; only the `gpp` command also reads a default from `config.toml`. The client sends the selected environment's trimmed copy of each operation, committed at build time. ([ADR 0006](adr/0006-merged-schema-runtime-environment.md))
- **Why a merged schema:** the environments differ, and generated code can match only one schema. Development is not a strict superset of production either: fields have existed only on production (23 of them at `a9f9755`). The merge pairs renamed types, takes the union with each part's availability, and gives production's type to every remaining conflict; a conflict is listed, never fatal. Docs and names follow development's view, since most users work there.
- **What an environment lacks:** a result field the selected environment lacks reads `None`; `is_available(model, "field")` or `client.is_available` tells that apart from a value GPP left null, and `client.enum_values(Enum)` gives the environment's values. Both answer from a generated availability table, without a network call.
- **Checks:** the only step before a generated operation is sent is the lookup of the selected environment's committed copy; an operation the environment lacks raises `NotAvailable` with nothing sent. Everything else goes to GPP as written, raw `execute` documents included, and GPP's answer is raised as `GPPGraphQLError`, `GPPHttpError` or `GPPTransportError` naming the environment. A scheduler REST path the environment does not serve gets GPP's 404, raised as `GPPHttpError` whose message adds that the path may not be served there.
- **Domains and the CLI** use only what both environments have. The every-operation test and ty enforce it: a domain reading a field one environment lacks fails the suite when the fake GPP for that environment omits it.

## Testing policy

| When | What runs | Network |
|---|---|---|
| Pull requests and merges | Mocked unit tests; every generated operation run on every environment against responses built from its committed schema; the build, which rejects operations that select what no environment has and trimmed copies invalid on their environment; the drift check, which rebuilds and fails when the committed generated code differs | None |
| Nightly (planned) | Live reads on development and production; live writes on development only, deleting only what the test created | Yes |

The plan keeps production free of live writes.

## Known gaps

Things the principles ask for that the code does not do yet:

- No test runs against a live server, and operations are only checked against schemas as old as the last schema update.
- Schema drift detection runs only by hand: `check_schema.yaml` compares each environment's live schema with the committed one when started, not on a schedule.
- Custom scalars (ids, timestamps, coordinates and the rest) are typed `Any` in the generated models, so users get no type checking on them, and a null where a model requires one parses without error.
- Coverage is incomplete: call-for-proposals operations exist in `graphql/operations/` with no domain or CLI command.
- AI agents get a hand-edited `llms.txt` (repo root, served at the docs root), but no usage skill.
- Releases are manual. The schema update is one command, but the job that would introspect, build and release on a schedule is deferred to later work.
- A variable declared nullable where an environment requires it fails the build by design: the build drops and lists what an environment lacks but never retypes a variable, so the operation is declared non-null instead. An operation is unavailable on an environment when any of its root fields is missing there.
- A field whose type differs between the environments reads `None` on development until the promotion; raw `execute` is the stopgap.
