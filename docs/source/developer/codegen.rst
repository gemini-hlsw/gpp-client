Code Generation
===============

The GPP Client uses `ariadne-codegen <https://github.com/mirumee/ariadne-codegen>`_
to generate the GraphQL transport client, operations, models, enums, input types,
fragments, and related API code.

All generated code lives in:

``src/gpp_client/generated/``


GraphQL Operations
------------------

Operations and fragments live in ``graphql/operations/shared/``. Each one is
written once and serves both environments, so a field that only development
has goes into the same query as everything else. The build trims it from the
copy that production receives, and it reads ``None`` there.


Running Codegen
---------------

Run the build from the repository root:

.. code-block:: bash

   uv run --group codegen python -m scripts.run_codegen

The build doesn't need a token, because it reads only the committed schemas.


What the Build Does
-------------------

1. It merges ``graphql/schemas/development.graphql`` and
   ``graphql/schemas/production.graphql`` into one schema. The merged schema is
   development's schema plus everything production still has. A type that the
   two environments name differently keeps development's name, and
   production's name stays importable as a deprecated alias. Where a field's
   type differs, production's type wins. The merged schema is never committed.
2. It fails, listing every case, when an operation selects something that
   neither environment has.
3. It runs ``ariadne-codegen`` once on the merged schema.
4. It trims every operation to each environment, checks each copy against
   that environment's schema, and writes the copies to ``generated/trimmed/``.
   At runtime the client sends the copy for the selected environment.
5. It writes ``generated/availability.py``, which lists the fields and enum
   values that some environment lacks, and ``generated/schema_commits.py``,
   which records the GPP commit each schema was downloaded at.

The build prints a merge summary and a trim summary. Paste them into the pull
request so reviewers can see what differs between the environments.


Codegen Configuration
---------------------

Code generation is configured in ``graphql/codegen.toml``. The build fills in
the schema, operations, and package paths itself.


Custom Plugins
--------------

The build uses these plugins from ``src/custom_plugins/``:

- ``AliasNamesPlugin`` keeps production's name for a renamed input type or enum
  as a deprecated alias.
- ``EnvironmentDefaultsPlugin`` gives a field that only some environments have
  a ``None`` default.
- ``AliasStrWrapperPlugin`` corrects alias behavior for wrapped scalar types.


Why Codegen Is Required
-----------------------

The GPP schema changes regularly. These changes may introduce:

- New input types
- New enums
- New fields
- Updated nullability
- New operations
- New custom types

Rather than manually maintaining the GraphQL layer, the client regenerates it
directly from the upstream schema.
