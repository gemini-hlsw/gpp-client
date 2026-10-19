CI checks
=========

These checks run on every pull request to ``main``, except the Schema Drift
Check. Each heading below is a check name as GitHub shows it. Read the Docs
runs its own check, and the others are GitHub Actions workflows in
``.github/workflows/``. A pull request can merge only when Run Lint and Tests
passes.

Run Lint and Tests
------------------

A failure means that Ruff's lint or format check, the ty type check, or a test
failed. The log names the problem. The tests also type-check the docs examples.
On ``main``, the tests also run on Python 3.12 to 3.14.

Two tests stand in for a check per environment. The every-operation test, in
``tests/gpp_client/client/test_every_operation.py``, sends every generated
operation through a fake GPP built from each committed schema and parses the
answer. A domain that reads a field one environment lacks gets ``None`` from
that environment's fake GPP, and ty flags an unguarded read of such a field,
because the merged schema makes it optional. So the domains and the CLI use
only what both environments have, or the check tells you where they don't.

These two commands fix most lint and format failures:

.. code-block:: bash

   uv run ruff check --fix .
   uv run ruff format .

Then run the type check and the tests:

.. code-block:: bash

   uv run ty check --error-on-warning src/gpp_client
   uv run pytest

Pre-commit
----------

A failure means that a hook failed on a file the pull request changes. Usually
the hooks aren't installed in your clone, so install them as described in
:doc:`setup`. Then run the hooks on every file and commit the files they fix:

.. code-block:: bash

   pre-commit run --all-files

Codegen Check
-------------

A failure means that the generated code, the committed schemas, or the
operations differ from a fresh build of the committed schemas. Someone edited generated files, or changed an
operation or a schema without rebuilding. To fix it, rebuild the client and
commit every file that ``git status`` lists:

.. code-block:: bash

   uv run --group codegen python -m scripts.build_client

Read the Docs
-------------

A failure means that the docs build warned. A warning is usually a broken
reference or a page that's missing from a table of contents. To find it, build
the docs locally, as described in :doc:`documentation`.

Schema Drift Check
------------------

This check doesn't run on pull requests. To see whether GPP's schema has
changed, start it by hand from the Actions tab. A failure isn't a bug. It means
that a schema update is due, which :doc:`updating-the-schema` describes.
