Project Setup
=============

This page describes how to set up a development environment for the GPP Client.

The project uses `uv <https://github.com/astral-sh/uv>`_ for dependency
management and execution. When running ``uv run``, a temporary environment is
created automatically based on the dependency groups defined in
``pyproject.toml``. No virtual environment activation is required.

Cloning the Repository
----------------------

.. code-block:: bash

   git clone https://github.com/gemini-hlsw/gpp-client.git
   cd gpp-client

Installing Dependencies
-----------------------

For full development (testing, docs, codegen, linting):

.. code-block:: bash

   uv sync --locked --all-groups

To install only development tools:

.. code-block:: bash

   uv sync --locked --dev

To install documentation tooling:

.. code-block:: bash

   uv sync --locked --group docs

To install schema-related tools:

.. code-block:: bash

   uv sync --locked --group schema

Pre-commit Hooks
----------------

Install ``pre-commit`` using ``uv``:

.. code-block:: bash

   uv tool install pre-commit --with pre-commit-uv

Install the repository hooks:

.. code-block:: bash

   pre-commit install

Run hooks manually:

.. code-block:: bash

   pre-commit run --all-files

These hooks validate:

- Ruff formatting and linting
- Python docstring rules via ``numpydoc``
- YAML/TOML/JSON correctness
- Test naming conventions
- No accidental commits to ``main``

Testing
-------

.. code-block:: bash

   uv run pytest

Tests run with ``asyncio`` enabled and use isolated import mode to ensure that
generated API code behaves correctly under real import conditions.
