---
status: accepted
---

# One generated client from a merged schema, environment chosen at runtime

Users need one install that reaches development and production, and GPP changes almost daily, so the generated client is built once from a merged schema and the user picks the environment at runtime. The merge and the generated client follow these rules:

- **One merged client.** Each environment's schema is committed once, inside the package (`src/gpp_client/schemas/`), by introspection of that environment's server. The build merges them into one schema that it never commits, and runs ariadne-codegen once on it. The merged schema is development's schema plus every element production still has.
- **Pairing with development's name and a production alias.** A type that production and development name differently is paired when the same parent type and field carry, on each side, a type of the same kind and list depth under a name the other side lacks; one vote per coordinate, iterated to a fixpoint, with no chained renames and no rename on an ambiguous vote. The generated class carries development's name; production's current name is a deprecated alias of the same class, in the input-types and enums modules, for as long as the pairing holds.
- **Production wins conflicts.** Where a field, argument or input field still differs by more than nullability, the merged schema takes production's type and the build lists the conflict. Where a type has a different kind on the two environments, production's definition wins and development-only elements typed by that name are dropped. The merge never fails.
- **`None` for what an environment lacks.** A result field the selected environment lacks reads `None`, with no sentinel and no validation context; inputs keep ariadne-codegen's `UNSET`. `is_available(model, "field")` and `client.enum_values(Enum)` answer from a generated availability table for the client's environment.
- **Build-time trim with committed copies.** Every generated operation is trimmed to each committed schema at build time and validated against it; the copies that differ, and a "missing" entry for an operation an environment lacks, are committed and looked up by digest at send time. The client sends the selected environment's copy, raises `NotAvailable` when the entry says the environment lacks the operation, and sends a raw `execute` document unchanged. There is no pre-send input check and no schema built at runtime.
- **Manual releases for now.** A schema update is one command, run by hand or by an agent; releases follow the developer docs' procedure. The automated release job is deferred.

## Considered Options

- **One generated subpackage per environment** (what GitHub Enterprise Server, the Kubernetes client and Stripe's typed SDKs do). Rejected after a proof of concept: three model classes per operation, so user code and domain return types differ by environment, a missing field raises `AttributeError`, and the wheel grew 2.8 times. Those SDKs target frozen versions; GPP's environments are one history at different points in time.
- **Typed production, loose development** (raw queries checked against the live schema). Rejected: development users would still need the per-environment trim, development features would go undocumented or be documented by hand, and code written against development would be rewritten after promotion.
- **Production's names for paired types.** Rejected: the same measured cost, but development users, the majority, would see the old name on 29% of days.
- **Fail the build on a conflict, and check every call before sending.** Rejected after replaying 190 days of schema pairs: a failing merge held every release hostage to one disputed field, and the pre-send check, the sentinel for absent fields, the typed per-environment views and the leaving-field warning were hand-written environment code for cases that the replay showed almost no consumer reaches.

## Consequences

- We own the merge, pairing and trim code. No maintained Python library merges schemas with a record of each part's environments; graphql-core supplies the building blocks.
- A development user whose field production types differently waits for promotion; raw `execute` is the stopgap.
- The client knows two environments, development and production. GPP promotes changes from development to staging to production, and the client sees only where a change starts and where it lands. The client does not reach staging: no user needs it, it would double the work of every change and schema update, and a stale staging schema could break the build.
- Releases are one stream with no pre-releases: every release matches each environment's schema on its date.

## Supersedes

ADR 0002 and the earlier version of this ADR.
