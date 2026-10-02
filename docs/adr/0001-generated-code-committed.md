# Generate the client with ariadne-codegen and commit the output

GPP's schema changes too often to maintain models, enums, input types and operation methods by hand. So the generated client is produced by ariadne-codegen, a generator that turns a GraphQL schema plus operations into typed Python, from downloaded schemas and hand-written `.graphql` operations. The output in `src/gpp_client/generated/` is committed, so a release is exactly what was reviewed and tested. Changes go into the operations or the codegen config, never into the output.

## Consequences

- Every operation change ships with its regenerated code in the same PR.
- Lint and pre-commit skip `generated/`.
- Swapping the generator would touch every domain, since domains call generated method and model names directly.
