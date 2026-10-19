# gpp-client

The Python client that lets Gemini's teams and their tools use GPP without tracking its fast-changing schema by hand.

## Platform

**GPP**:
The Gemini Program Platform, the system whose API this client calls. The word users and docs use for the API.
_Avoid_: the backend, the API server

**ODB**:
The lucuma ODB, the GPP server that serves the GraphQL API and REST paths. Use only when the server itself is meant.
_Avoid_: GPP (when meaning the server), lucuma

**Environment**:
One of the two GPP deployments the client reaches: development or production. GPP also runs staging, which the client doesn't reach.
_Avoid_: server, instance, stage

**Schema**:
The GraphQL type system an environment exposes at a point in time.

**Environment-specific**:
Present in some environments but not all: an operation, field, enum value, input field, or REST path. Either environment can have things the other lacks.
_Avoid_: development-only, dev-only (for the general case)

**Merged schema**:
One schema combining both environments' schemas after pairing, recording which environments have each part, with production's type where the two disagree. The generated client is built from it; the build never commits it.
_Avoid_: union schema, superset schema

**Pairing**:
The build's matching of a production type to the development type that replaced it under a new name, when the same field, argument, or input field carries each name on its side and neither side has the other's name. The merged schema uses development's name; the pairing is the alias list.
_Avoid_: rename map, type mapping

**Alias**:
Production's current name for a paired input type or enum, generated as a deprecated alias of the development-named class. It exists in exactly the releases whose pairing contains the rename.
_Avoid_: shim, compatibility name

**Conflict**:
A field, argument, or input field whose type differs between the environments by more than nullability. The merged schema takes production's type and the build lists it; a kind conflict is a type name that means a different kind of type on each environment, where production's definition wins.
_Avoid_: mismatch, incompatibility

**Availability**:
The set of environments that have a given operation, field, enum value, or input field. The build writes it to a generated table, which `is_available` and `enum_values` read.
_Avoid_: support (ambiguous with what the client supports)

**Promotion**:
GPP moving changes forward one environment, from development to staging and from staging to production. The client doesn't reach staging, so it sees a promotion when a change reaches production. Most environment-specific things are changes waiting for promotion.
_Avoid_: deploy (for this step), release (that word is the client's)

**Leaving**:
Removed from development but still on production, so expected to leave production at a coming promotion. The removal shows under development's "Breaking" list in the release notes and in the merge summary the schema update prints; there is no runtime warning.
_Avoid_: deprecated (GPP's own deprecation is a separate thing)

## Client

**Operation**:
A hand-written GraphQL query, mutation, or subscription that the client is generated from.
_Avoid_: query (for all three kinds)

**Generated client**:
The code produced from the schema and operations by code generation.
_Avoid_: GraphQL layer, API code

**Domain**:
A hand-written group of task-shaped methods for one area of GPP, such as programs or scheduling.
_Avoid_: manager, resource manager, orchestration layer

**Curated convenience**:
A hand-written method that does more than call one generated method, such as combining GraphQL and REST results.
_Avoid_: helper, wrapper

## Change and release

**Schema update**:
One command that introspects both environments, holds an environment whose schema doesn't build, rebuilds the generated client from the merged schema, and runs the tests.
_Avoid_: schema sync, regen

**Hold**:
A schema update keeping an environment's committed schema because the one it introspected doesn't build. The update names the held environment, and the release notes carry it.
_Avoid_: skip, freeze

**Release**:
A published package version matching each environment's schema on its date. Releases are one stream, made by hand from the developer docs' procedure.
_Avoid_: pre-release, dev release, beta (there are none; see [ADR 0006](adr/0006-merged-schema-runtime-environment.md))
