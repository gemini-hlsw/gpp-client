# Version with CalVer taken from the git tag

The package uses calendar versioning, `YY.M.PATCH` (for example `26.9.0`, month without a leading zero), with a `.devN` suffix for pre-releases. The version comes from the git tag through uv-dynamic-versioning, a build plugin that reads it at build time, rather than from `pyproject.toml`. The original reasons were not written down. What the scheme gives us now: the version says how old a client is relative to a GPP schema that keeps moving, and it makes no compatibility promise that GPP's pace would break (ADR 0005).
