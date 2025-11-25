Continuous Schema Monitoring
============================

The GPP schema evolves continuously. To ensure that the client remains
compatible, the repository includes a nightly workflow that downloads schemas
from multiple environments and compares them against committed versions.

Nightly Workflow
----------------

The workflow runs at midnight UTC and may also be triggered manually.

It performs:

1. Schema download for each configured environment
2. Comparison against committed schema
3. Reporting of breaking, dangerous, or safe changes

How Results Are Used
--------------------

- **Production schema changes** fail the workflow if the change is breaking.
- **Development schema changes** do not fail the workflow.
  This environment often contains in-progress features and may change without
  notice.

Maintainers should:

- Inspect reported diffs
- Run ``scripts/run_codegen.py`` if required
- Commit updated schema files and regenerated client code