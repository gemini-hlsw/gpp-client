---
status: accepted, implemented
---

# One generated client from a merged schema, environment chosen at runtime

Users need one install that reaches development and production, and GPP changes almost daily, so the generated client is built once from a merged schema: every environment's schema combined, recording which environments have each operation, field, enum value and input field. At build time each operation gets a trimmed copy per environment, with the parts that environment lacks removed; at runtime the client sends the copy for the selected environment. In a generated operation, a field the environment lacks reads `None`. Anything else the environment lacks (an operation, an argument, a set input field, an enum value), or requires and the call leaves unset, raises an error before sending. A query-builder call or raw document is checked as written, so a field it selects that the environment lacks raises too.

## Considered Options

- **One generated subpackage per environment** (what GitHub Enterprise Server, the Kubernetes client and Stripe's typed SDKs do). Rejected after a proof of concept: three model classes per operation, so user code and domain return types differ by environment, a missing field raises `AttributeError`, and the wheel grew 2.8 times. Those SDKs target frozen versions; GPP's environments are one history at different points in time.
- **Typed production, loose development** (raw queries checked against the live schema). Rejected: development users would still need the per-environment trim, development features would go undocumented or be documented by hand, and code written against development would be rewritten after promotion.

## Consequences

- We own the merge and trim code. No maintained Python library merges schemas with a record of each part's environments; graphql-core supplies the building blocks.
- Conflicts follow fixed rules: differing output nullability becomes nullable; differing input or argument nullability becomes optional, with a runtime check against the selected environment; a field whose type differs, or that has an argument whose type differs, is left out, and the build fails if an operation selects it; a type of a different kind fails the merge.
- The client knows two environments, development and production. GPP promotes changes from development to staging to production, and the client sees only where a change starts and where it lands. The client does not reach staging: no user needs it, it would double the work of every change and schema update, and a stale staging schema could break the build. The "coming to production" signal, `GPPFieldLeavingWarning`, is built on development.
- Releases are one stream with no pre-releases: every release matches each environment's schema on its date.
