Releases
========

The project uses **Calendar Versioning (CalVer)** rather than Semantic Versioning.

Version format:

``YY.MM.PATCH``

Examples:

- ``25.11.0``
- ``25.12.2``

Development releases
--------------------

Development releases follow CalVer but include a ``.devN`` suffix,
for example:

- ``25.11.0.dev1``
- ``25.11.0.dev2``

Why CalVer?
-----------

GPP evolves continuously, and the GPP Client must track the upstream schema.
Calendar versioning reflects the release cadence, simplifies compatibility
tracking, and avoids the overhead of interpreting breaking vs. non-breaking
changes in a schema-driven ecosystem.

Release Workflow
----------------

Releases in ``gpp-client`` follow a **pull request-based workflow**.

1. Create a PR targeting either:

   - ``dev`` for a development (``.devN``) release, or
   - ``main`` for a production release.

2. In the PR, bump the version using:

   .. code-block:: bash

      uv version <VERSION>

   This updates both ``pyproject.toml`` and ``uv.lock``. No manual editing is
   required.

3. Include any changelog or documentation updates in the same PR.

4. Once all the checks pass, merge the PR.

Tagging and Drafting the Release
--------------------------------

After the PR is merged, a maintainer must trigger the **Create Release** workflow.

To trigger:

1. Navigate to **Actions → Create Release**.
2. Click **Run workflow**.
3. Enter:

   - ``version`` (e.g., ``25.11.0`` or ``25.11.0.dev1``)
   - ``base_branch`` (``main`` or ``dev``)

4. Click **Run workflow**.

The workflow will:

- Check out the selected branch
- Create a Git tag (``v<VERSION>`` — the workflow automatically adds the ``v`` prefix)
- Push the tag
- Create a **draft GitHub Release** with auto-generated notes

The workflow does *not* modify or commit files.

Publishing
----------

After the workflow completes:

1. Open **Releases** on GitHub.
2. Select the draft release created for the tag.
3. Review the generated notes.
4. Click **Publish**.

PyPI publication is handled separately (for example, via a dedicated publish
workflow), but is fully automated once triggered.
