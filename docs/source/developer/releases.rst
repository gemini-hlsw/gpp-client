Releases
========

The project uses **Calendar Versioning (CalVer)** rather than Semantic
Versioning.

Version format:

``YY.MM.PATCH``

Examples:

- ``25.10.0``
- ``25.11.2``

Why CalVer?
-----------

GPP evolves continuously, and the GPP Client must track the upstream schema.
Calendar versioning reflects the release cadence, simplifies compatibility
tracking, and avoids the overhead of interpreting breaking vs. non-breaking
changes in a schema-driven ecosystem.

Release Workflow
----------------

Releases are created using the **Create Release** GitHub Action.

To trigger:

1. Navigate to **Actions → Create Release**.
2. Click **Run workflow**.
3. Enter the new version (e.g., ``25.10.4``).
4. Click **Run workflow**.

The workflow will:

- Update ``pyproject.toml`` with the new version
- Regenerate ``uv.lock``
- Commit and push the version bump
- Create a Git tag
- Draft a GitHub release

Publishing
----------

After the workflow completes:

1. Open **Releases** on GitHub.
2. Select the draft release.
3. Click **Publish**.

PyPI publication happens automatically.