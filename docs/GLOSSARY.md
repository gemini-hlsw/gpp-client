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
One of GPP's three deployments: development, staging, or production.
_Avoid_: server, instance, stage

**Schema**:
The GraphQL type system an environment exposes at a point in time.

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
Downloading an environment's current schema and regenerating the generated client from it.
_Avoid_: schema sync, regen

**Release**:
A published package version matching the production schema on its date.

**Pre-release**:
A published package version matching the development schema on its date.
_Avoid_: dev release, beta
