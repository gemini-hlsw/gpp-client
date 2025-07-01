Developer Guide
===============

This page documents how to maintain and develop the GPP Client.

Overview
--------

The GPP Client uses `uv <https://github.com/astral-sh/uv>`_ to manage dependencies and execute scripts.

When using ``uv run``, a temporary virtual environment is created with only the dependencies required to run the script, based on the groups defined in ``pyproject.toml``.

There's no need to manually create or activate a virtual environment, ``uv`` handles everything.

Set Up ``pre-commit``
---------------------

Install ``pre-commit`` using ``uv``:

.. code-block:: bash

   uv tool install pre-commit --with pre-commit-uv

.. note::

   You may be prompted to add ``~/.local/bin`` to your ``PATH``. ``uv`` installs tools there by default.

Install the hooks defined in ``.pre-commit-config.yaml``:

.. code-block:: bash

   pre-commit install

Once installed, ``pre-commit`` will automatically run the configured hooks each time you commit changes.
This helps catch formatting issues, docstring violations, and other problems before code is committed.

To manually run all hooks on the entire codebase:

.. code-block:: bash

   pre-commit run --all-files

Download the Schema
-------------------

This script downloads the latest GPP GraphQL schema to ``schema.graphql``.

.. code-block:: bash

   uv run --group schema python scripts/download_schema.py

.. note::

   You must have the environment variables ``GPP_URL`` and ``GPP_TOKEN`` set for this script to work.

Run Codegen
-----------

This script regenerates the client code based on the updated schema.

.. code-block:: bash

   uv run --group codegen python scripts/run_codegen.py

Create and Deploy a Release
---------------------------

Releases are managed using GitHub Actions. Use the **Create Release** workflow to publish a new version.

Triggering a Release
~~~~~~~~~~~~~~~~~~~~

1. Go to the **Actions** tab on GitHub.
2. Select the **Create Release** workflow.
3. Click **Run workflow**.
4. Enter the new version (e.g., ``25.6.0``) in the prompt.
5. Click **Run workflow** to begin.

.. note::

   Do **not** include a leading ``v`` or unnecessary zero padding in the version.

This workflow will:

- Update the ``version`` field in ``pyproject.toml``.
- Update ``uv.lock`` to reflect the new version.
- Commit and push the version bump.
- Create a Git tag.
- Draft a GitHub release.

Finalize the Release
~~~~~~~~~~~~~~~~~~~~

After the workflow completes:

1. Go to the **Releases** section on GitHub.
2. Locate the new draft release.
3. Click **Publish release**.

Once published, the package will be uploaded to `PyPI <https://pypi.org/project/gpp-client/>`_.

.. note::

   It may take a few minutes for the release to appear on PyPI.