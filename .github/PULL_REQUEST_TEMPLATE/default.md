<!--
General pull request.

Versioning:
- Do not bump the version in default PRs.
- Version changes only occur in release PRs using `uv version`.

Docs:
- If your change affects documentation, run the live docs server:
    uv sync --group docs
    uv run sphinx-autobuild docs/source docs/build
- Then open:
    http://127.0.0.1:8000
- This rebuilds automatically on file changes.

Testing:
- Run linting and tests locally before requesting review.
    uv run --dev pytest

-->

## Checklist
- [ ] Linting and tests pass.
- [ ] If this PR changes GraphQL types or queries, the codegen has regenerated the  models.
- [ ] Documentation builds cleanly (if docs were modified).
