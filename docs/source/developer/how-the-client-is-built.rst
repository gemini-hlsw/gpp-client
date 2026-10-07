How the client is built
=======================

Why codegen
-----------

GPP changes its GraphQL schema almost every day: new fields, new enum values,
new input types, and changed nullability. A GraphQL layer written by hand
couldn't keep up. So the project generates most of the client from the schema
with `ariadne-codegen <https://github.com/mirumee/ariadne-codegen>`_, and the
hand-written domain classes and CLI sit on top of it.

One install of the client works with development and production, and the user
selects the environment at runtime. The build makes that possible from one set
of operations.

Files you write
---------------

``graphql/operations/``
   Every GraphQL operation and fragment, grouped by domain. You write each one
   once for all environments, so never sort operations by environment.

``graphql/codegen.toml``
   The ariadne-codegen settings and the list of plugins. The build fills in the
   paths.

``src/gpp_client/domains/``
   One module per domain, such as ``client.program``. Each method wraps a
   generated method, as :doc:`adding-a-call` shows.

``src/gpp_client/cli/``
   The ``gpp`` command-line tool.

``src/gpp_client/rest/``
   The client for GPP's REST endpoints, which domains such as attachments use.

Files you download
------------------

``graphql/schemas/<environment>.graphql``
   The development and production schemas. Change them only by
   downloading them again, as described in :doc:`updating-the-schema`.

Files the build writes
----------------------

Never edit these files by hand. Rebuild instead, and commit them with the
change that caused them.

``graphql/schemas/merged.graphql``
   The two environment schemas, merged into one schema.

``src/gpp_client/generated/``
   The generated client, models, enums, and input types.

``src/gpp_client/generated/trimmed/``
   The list of generated operations, and for each environment a copy of each
   operation that the environment receives trimmed or can't run.

``src/gpp_client/generated/schemas/``
   The development and production schemas, without descriptions, for checks at
   runtime.

``llms.txt``
   A summary for AI agents, including what only one environment has.

The build, step by step
-----------------------

One command runs every step:

.. code-block:: bash

   uv run --group codegen python -m scripts.build_client

Merged schema
   The build merges the two environment schemas into one. Every type, field,
   argument, and enum value that isn't on both gets an
   ``@environments(names: [...])`` marker, which names the environments that
   have it.

One codegen run
   ariadne-codegen runs once, on the merged schema. So the generated code is
   the same whichever environment the user selects.

Trimmed operations
   For each environment, the build removes the fields, arguments, and
   fragments that the environment lacks from every operation. If the
   environment lacks an operation's root field, the build marks that operation
   unavailable there. The build checks each trimmed copy against that
   environment's schema. At runtime, the client sends the copy for the
   selected environment.

Checks before sending
   The build bundles each environment's schema in the package. Before the
   client sends a call, it checks the call against the schema of the selected
   environment. It checks a generated operation as its trimmed copy, and a
   query-builder or raw call as written.

   If the call needs something that the selected environment lacks but another
   environment has, the client raises ``GPPEnvironmentError`` and doesn't send
   the call. If no environment has it, as with a misspelled field, the client
   sends the call and GPP returns the error.

   The client also issues a ``GPPFieldLeavingWarning`` when the call selects a
   field that development has already removed, because that field will soon
   leave the selected environment.

Plugins
-------

The project's own ariadne-codegen plugins live in ``src/custom_plugins/``, and
``graphql/codegen.toml`` lists them:

``AliasStrWrapperPlugin``
   Wraps input field aliases in ``str()`` so that editors type-check them.

``TolerantEnumsPlugin``
   Lets an enum accept a value that GPP added after the client was built, so
   installed clients keep working.

``CaptureOperationsPlugin``
   Hands the build each operation exactly as the generated client embeds it,
   so that trimming starts from the same text.

``EnvironmentDefaultsPlugin``
   Makes a result field default to ``None`` when some environments lack it.

``AvailabilityDocstringsPlugin``
   Starts the docstring of everything that only one environment has with
   ``Available on: <environments>.``, which the docs show as a badge.
