# GPP-Client Release Pull Request
<!-- This pull request prepares a new **GPP-Client** release. -->

## Versioning
- [ ] Bump the version using `uv version <VERSION>` (this updates `pyproject.toml` and `uv.lock`).
- [ ] For production releases: version follows `YY.MM.PATCH` (e.g., `25.11.0`).
- [ ] For development releases: version must have `devN` suffix. (e.g., `25.11.0.dev1`).

## Documentation
- [ ] Build documentation locally and confirm no warnings or link issues.
```console
uv run --group docs sphinx-autobuild docs/source docs/build
```

## Validation
- [ ] Generated types (`ariadne-codegen`) are up to date.
- [ ] All tests pass on CI.

## Final Checks
- [ ] PR is labeled as a release-preparation PR.

## Post-Merge (informational)
After this pull request is merged:

- Run the **Create Release** workflow from GitHub Actions.
- The workflow will create:
  - A properly versioned Git tag
  - A draft GitHub Release with auto-generated notes
- Make sure to publish the release and properly mark if a pre-release if development

No additional commits should be pushed to the branch between merging this PR and running the release workflow.
