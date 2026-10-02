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
4. **All three environments.** Users should reach development, staging or production from one install and switch easily. Not met today - see [Environments](#environments).

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

There is no announcement channel. We plan to watch the GitHub Deployments API, which records the commit live in each environment, and back it up with a nightly check of each live server's schema.

## Data sources

| Source | What we use it for | Reached through |
|---|---|---|
| ODB GraphQL (`/odb`) | Programs, observations, targets, attachment metadata, workflow state, GOATS and scheduler queries | Generated client |
| ODB GraphQL subscriptions (`/ws`) | Live edits to programs, observations and targets; scheduler calculation updates | Generated client |
| ODB REST | Scheduler atom digests and visibility changes; attachment upload and download | `gpp_client.rest` |
| gemini.edu status pages | Site and instrument status (`client.site_status`) | HTML/JSON scraping, not GPP |

## Release contract

A release matches the production schema on its release date. A `.devN` pre-release matches the development schema on its date. Neither is guaranteed to work against GPP weeks later. Users should upgrade often.

When GPP removes or renames something, the break reaches users on their next upgrade. We keep no shims (adapters that keep old names working); release notes name what changed. ([ADR 0005](adr/0005-schema-breaks-pass-through.md))

Versions are CalVer (calendar versioning, `YY.M.PATCH`, such as `26.9.0`), set from the git tag. ([ADR 0003](adr/0003-calver-from-git-tags.md))

## Environments

GPP runs three environments: development, staging and production.

- **Today:** the generated client is built for development or production, never both, and that choice is made when the package is built. A pre-release carries development code; a release carries production code. Staging is not supported. ([ADR 0002](adr/0002-environment-fixed-at-build-time.md))
- **Why:** some operations exist only on development, and generated code matches one schema. Development is not a strict superset of production either: fields have existed only on production (23 of them at `a9f9755`).
- **Goal:** one install that reaches all three environments, with easy switching.
- **Status:** open problem, no chosen design. It gets its own design session and an ADR that supersedes ADR 0002.

## Testing policy

| When | What runs | Network |
|---|---|---|
| Pull requests and merges | Mocked unit tests; codegen, which rejects operations that don't match the committed schemas | None |
| Nightly (planned) | Live reads on all three environments; live writes on development and staging, deleting only what the test created | Yes |

The plan keeps production free of live writes.

## Known gaps

Things the principles ask for that the code does not do yet:

- Staging is unsupported, and the environment is fixed at build time.
- No test runs against a live server, and operations are only checked against schemas as old as the last schema update.
- Schema drift detection is not running: the schema-check workflows are manual-only and do not work as written.
- The codegen check in CI regenerates code but does not fail when the committed code differs.
- Coverage is incomplete: call-for-proposals operations exist in `graphql/operations/` with no domain or CLI command.
- Nothing yet helps AI agents use the library, such as an `llms.txt` or a usage skill.
- Parts of the README and the Sphinx docs describe older behavior.
