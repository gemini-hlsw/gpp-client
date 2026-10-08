Documentation
=============

Sphinx builds the site from ``docs/source/``, and Read the Docs hosts it. Most
of the reference is generated: autodoc reads the docstrings, and the CLI pages
come from the commands themselves. Write by hand only what the code can't say.

Build the docs locally
----------------------

This command builds the site, serves it at http://127.0.0.1:8000 and rebuilds
it when a file changes:

.. code-block:: bash

   uv run --group docs sphinx-autobuild docs/source docs/build

A full build takes about two minutes. For a one-off build without a server,
run:

.. code-block:: bash

   uv run --group docs sphinx-build -W -j auto -b html docs/source docs/build

The ``-W`` flag turns warnings into errors, as on Read the Docs, so any warning
fails the docs check on your pull request.

Read the Docs builds a preview of each pull request. The ``latest`` version
follows ``main`` and shows a banner saying that it may describe changes that
aren't released yet. The ``stable`` version is the latest release.

Availability badges
-------------------

Some operations, types, fields, input fields, and enum values exist on only
one environment. The
build starts their docstrings with ``Available on: <environments>.``, and the
Sphinx extension in ``docs/source/_ext/availability_badge.py`` shows that line
as a badge with one colored pill per environment. Anything on both development
and production gets no badge.

Class tables
------------

The input types, result models, and field builders pages each start with a
table of their classes. The ``.. class-index::`` directive, from
``docs/source/_ext/class_index.py``, builds that table from the classes on the
page.

Never write availability or a list of classes by hand. Whatever the schema
decides - operations, fields, enum values, which environment has what -
reaches the docs only through generated output, so it stays correct after each
schema update.

Add an example
--------------

1. Write a normal Python block on the page:

   .. code-block:: rst

      .. code-block:: python

         result = await client.program.get_by_id("p-123")
         print(result.program)

   The name ``client`` is already defined, and ``await`` works. Import or
   define every other name that the block uses, in the block.

2. Check the example:

   .. code-block:: bash

      uv run pytest tests/docs

   A failure names the page and line.

The test type-checks every Python block with ty, so it catches a misspelled
method, a wrong argument or an undefined name. It doesn't run the example, so
it can't catch a wrong result.

A block with no language, or a paragraph ending in ``::``, counts as Python.
Use ``.. code-block:: text`` for anything else, and ``bash`` for shell
commands.

To skip one block, for example a traceback, put this comment right above it:

.. code-block:: rst

   .. docs-guard: skip - shows a traceback, not code to run

The README quickstart shows the lines of the Getting started example. Change
both together, because ``tests/docs/test_readme.py`` fails when the README
stops showing them.

Keep the site self-contained. The ``tests/docs/test_docs_guard.py`` test fails
when a page points to the maintainers' design notes: the ADR and agent folders
under ``docs/``, or the glossary, architecture, overview and agent instruction
``.md`` files.
