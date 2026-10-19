# Version with CalVer taken from the git tag

The package uses calendar versioning, `YY.M.PATCH` (for example `26.9.0`, month without a leading zero), with no pre-release suffix ([ADR 0006](0006-merged-schema-runtime-environment.md)). The version comes from the git tag through uv-dynamic-versioning, a build plugin that reads it at build time, rather than from `pyproject.toml`. The scheme says how old a client is relative to a GPP schema that keeps moving, and it makes no compatibility promise that GPP's pace would break (ADR 0005).
