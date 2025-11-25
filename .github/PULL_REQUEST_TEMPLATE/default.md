<!--
General pull request.

Branching:
- Development-only changes should target `dev`.
- Production-ready changes should target `main`.

Versioning:
- Do not bump the version in default PRs.
- Version changes only occur in release PRs using `uv version`.

Schema:
- If your change affects GraphQL models, run codegen locally
  to ensure all generated types are up-to-date.

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

## Summary
<!-- Describe the purpose of this change. -->

## Testing
<!-- Explain how you validated this change. -->

## Checklist
- [ ] This PR targets the correct branch (`dev` for development changes, `main` for production).
- [ ] Linting and tests pass.
- [ ] If this PR changes GraphQL types or queries, the codegen has regenerated the  models.
- [ ] Documentation builds cleanly (if docs were modified).
