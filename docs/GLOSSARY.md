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
One schema combining every environment's schema, recording which environments have each part. The generated client is built from it.
_Avoid_: union schema, superset schema

**Availability**:
The set of environments that have a given operation, field, enum value, or input field.
_Avoid_: support (ambiguous with what the client supports)

**Promotion**:
GPP moving changes forward one environment, from development to staging and from staging to production. The client doesn't reach staging, so it sees a promotion when a change reaches production. Most environment-specific things are changes waiting for promotion.
_Avoid_: deploy (for this step), release (that word is the client's)

**Leaving**:
Removed from development but still on production, so expected to leave production at a coming promotion.
_Avoid_: deprecated (GPP's own deprecation is a separate thing), production-only

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
Downloading every environment's current schema and rebuilding the generated client from their merged schema.
_Avoid_: schema sync, regen

**Release**:
A published package version matching each environment's schema on its date. Releases are one stream.
_Avoid_: pre-release, dev release, beta (there are none; see [ADR 0006](adr/0006-merged-schema-runtime-environment.md))
