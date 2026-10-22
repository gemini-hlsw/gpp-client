# GraphQL operations

Operations and fragments live in `operations/shared/`. Each one is written once and serves both GPP environments; the build trims what an environment lacks from the copy it sends there.

The schemas the operations are built against live in `schemas/`, one per environment.

To rebuild the client after changing an operation or a schema, run from the repository root:

```bash
uv run --group codegen python -m scripts.run_codegen
```

The developer guide covers the build and schema updates:

https://gpp-client.readthedocs.io/en/latest/developer/codegen.html
