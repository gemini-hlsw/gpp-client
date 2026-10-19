Setup
=====

This page takes you to a working checkout: the code, its dependencies, the
commit hooks, and a passing test run.

The project uses `uv <https://github.com/astral-sh/uv>`_ to manage Python,
dependencies, and commands, and it needs uv 0.11 or newer. The ``uv run``
command runs a command in the project's environment, so there's nothing to
activate.

Clone the repository
--------------------

Clone the repository and change into its folder:

.. code-block:: bash

   git clone https://github.com/gemini-hlsw/gpp-client.git
   cd gpp-client

Install the dependencies
------------------------

This command installs the package and every dependency group: development
tools, codegen, schema download, and docs:

.. code-block:: bash

   uv sync --locked --all-groups

The ``--locked`` flag uses the exact versions in ``uv.lock``.

Install the commit hooks
------------------------

Install pre-commit, then install the hooks in your clone:

.. code-block:: bash

   uv tool install pre-commit --with pre-commit-uv
   pre-commit install

On each commit, the hooks run Ruff, the numpydoc docstring check, a check that
``uv.lock`` matches ``pyproject.toml``, and a few file checks. They also refuse a commit on ``main``. When a hook fixes a file, the
commit stops, so stage the file and commit again.

Run the tests
-------------

Run the whole test suite:

.. code-block:: bash

   uv run pytest

The tests print one line each and end with a summary of how many passed and
failed. They run in parallel and offline, so they never call GPP or its REST
services.
