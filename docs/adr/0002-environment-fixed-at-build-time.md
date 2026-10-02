# Fix the GPP environment when the package is built

Generated code can match only one schema, and development has operations production lacks. So codegen runs for one environment and records it in `generated/package_environment.py`, and the installed package targets that environment. A `.devN` pre-release carries development code, a release carries production code, and `scripts/validate_release.py` refuses a tag whose generated code does not match.

This records the current design, not the goal. Its known costs: staging is unsupported; reaching another environment means installing a different version (the `environment_override` setting moves the server but not the generated code); and `main` alternates between development and production code around each release. Replacing it is an open problem (`docs/OVERVIEW.md`, Environments), and the ADR that decides the replacement supersedes this one.
