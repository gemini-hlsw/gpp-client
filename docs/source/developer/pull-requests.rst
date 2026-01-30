Pull Request Templates
======================

This project uses **multiple GitHub pull request templates** to ensure that
changes follow the correct workflow, validation steps, and release process.

**Selecting the correct template is mandatory.**
Each template contains required instructions and checklists that reviewers
and CI rely on.

Why This Matters
----------------

GitHub does **not** automatically switch pull request templates after a PR
is created.

If the wrong template is used:

- Required steps may be skipped.
- CI or release workflows may fail.
- The PR may be blocked until corrected or recreated.

For this reason, **the template must be selected before creating the pull request**.

Template Selection Flow
-----------------------

When opening a new pull request on GitHub, you will see the following message:

.. code-block:: markdown

  <!--
  Thank you for contributing to gpp-client!

  Please select the appropriate pull request template below.
  This helps maintain project consistency and ensures PRs go through
  the correct checks and release workflow.
  -->

  ### Choose a template:

  - [Default](?expand=1&template=default.md) — for all development and feature changes.
  - [Release](?expand=1&template=release.md) — for version bumps and release preparation.

**You must follow these steps exactly:**

1. Click **Preview** (not "Create pull request").
2. Click the link that matches the type of PR you are creating.
3. Verify that the PR body updates with the selected template.
4. Only then click **Create pull request**.

.. warning::

  Selecting a template **after** creating the pull request will **not**
  update the PR body.
  If the wrong template is used, the PR may need to be closed and recreated.

Template Overview
-----------------

Default Pull Request Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the **Default** template for:

- Feature development
- Bug fixes
- Refactors
- Internal improvements
- Documentation updates (non-release)

Key rules enforced by this template:

- **Do not bump versions** in default PRs.
- GraphQL changes require local code generation.
- Documentation changes must build cleanly.
- Linting and tests must be run before review.

.. warning::
  Do **not** use this template for release-related changes such as version bumps.

This template ensures development work remains isolated from release logic.

Release Pull Request Template
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the **Release** template **only** for:

- Version bumps
- Release preparation
- Final validation before publishing

Key rules enforced by this template:

- Version must be bumped using ``uv version``.
- Versioning must follow:

  - ``YY.MM.PATCH`` for production releases
  - ``YY.MM.PATCH.devN`` for development releases

- Documentation must build without warnings.
- Schema drift and generated types must be validated.
- The PR must be correctly labeled.

This template directly supports the automated release workflow.

See :doc:`Releases <releases>` for more details on the release process.