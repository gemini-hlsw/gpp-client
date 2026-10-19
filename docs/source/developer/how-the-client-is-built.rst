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

``src/gpp_client/schemas/<environment>.graphql``
   The development and production schemas, each committed once, inside the
   package, so installs carry them. Change them only by downloading them
   again, as described in :doc:`updating-the-schema`. The first line is a
   comment, ``# schema-date: YYYY-MM-DD``, with the day the schema was
   introspected, so a reader of the file knows how current it is.

Files the build writes
----------------------

Never edit these files by hand. Rebuild instead, and commit them with the
change that caused them.

``src/gpp_client/generated/``
   The generated client, models, enums, and input types.

``src/gpp_client/generated/trimmed/``
   The list of generated operations, and for each environment a copy of each
   operation that the environment receives trimmed or can't run.

``src/gpp_client/generated/availability.py``
   The result-model fields and the enum values that some environment lacks,
   each with the environments that have it. ``is_available`` and
   ``enum_values`` read it; anything not listed is on every environment.

The build, step by step
-----------------------

One command runs every step:

.. code-block:: bash

   uv run --group codegen python -m scripts.build_client

Merged schema
   The build merges the two environment schemas into one, in three steps.

   First it pairs renamed types. When the same field, argument, or input
   field carries a type of the same kind and list depth under a different
   name on each environment, and neither environment has the other's name,
   the production type takes development's name. Each such place votes once;
   a type whose votes disagree, or whose development name another rename
   already took, keeps its name and the build lists it. The build repeats the
   step until it finds nothing new, and a renamed type is never renamed again.

   Then it takes the union of both schemas. Every type, field, argument, input
   field, and enum value that isn't on both gets an
   ``@environments(names: [...])`` marker, which names the environments that
   have it, and is nullable or optional in the merged schema.

   Last, production wins every remaining conflict. A field, argument, or
   input field whose type still differs takes production's type and is marked
   as production's. A type name that means a different kind of type on each
   environment takes production's definition, and the parts of development's
   schema typed by that name are dropped. The build lists every conflict and
   never fails on one. Descriptions and deprecations come from development
   where it has the element, from production otherwise.

   The merged schema is a build intermediate: it's never committed.

One codegen run
   ariadne-codegen runs once, on the merged schema. So the generated code is
   the same whichever environment the user selects.

   A paired input type or enum keeps development's name, and production's
   current name becomes a deprecated alias of the same class in
   ``input_types.py`` and ``enums.py``. Importing the alias works, type
   checkers resolve it, and it warns once per line with the new name. The
   build lists each alias with its target in the merge summary. The alias
   list is the pairing of that build, so it goes away in the first release
   after GPP promotes the rename.

Trimmed operations
   For each environment, the build takes every operation as the generated
   client embeds it and removes what that environment lacks: fields,
   arguments, fields and enum values inside input literals, and inline
   fragments and fragment spreads on a type the environment lacks or that can
   never apply there. A variable left unused goes too, and a selection set
   left empty keeps ``__typename``. The development copy also drops a field,
   argument, or input field whose type differs between the environments,
   because the generated client carries production's type for it. The
   production copy names a renamed type as production still does, in fragment
   conditions and variable types.

   If the environment lacks any of an operation's root fields, the build marks
   the whole operation unavailable there, so a mutation never runs half of
   its root fields. The build never changes a variable's declared type: an
   operation that declares a variable nullable where an environment requires
   it fails the build, and you declare it non-null instead.

   The build checks each copy against that environment's schema and fails if
   one breaks a rule there. It commits a copy only where it differs from the
   generated text, plus a "missing" entry for each unavailable operation, and
   looks each up by a digest of the generated text. At runtime, the client
   sends the copy for the selected environment.

Availability table
   The build writes ``generated/availability.py`` from the merged schema: each
   result-model field that ``EnvironmentDefaultsPlugin`` defaulted to ``None``,
   and each enum value, with the environments that have it. A field or value
   on every environment is not listed. At runtime ``is_available(model,
   "field")`` and ``client.enum_values(Enum)`` answer from it, so a user
   branches on an environment difference without a network call.

What the client sends
   The lookup of the selected environment's copy is the only step before a
   generated operation goes out. The client sends the copy, or raises
   ``NotAvailable`` without sending when the entry says the environment
   lacks the operation. A raw document given to ``client.graphql.execute``
   goes out unchanged. The client doesn't check inputs against the schema:
   GPP rejects what the environment can't take, and the client raises that
   answer as a ``GPPError`` naming the environment.

Plugins
-------

The project's own ariadne-codegen plugins live in ``src/custom_plugins/``, and
``graphql/codegen.toml`` lists them:

``AliasNamesPlugin``
   Adds production's name for each paired input type and enum as a deprecated
   alias of the generated class, and lists it in the package's ``__all__``.

``TolerantEnumsPlugin``
   Lets an enum accept a value that GPP added after the client was built, so
   installed clients keep working.

``EnvironmentDefaultsPlugin``
   Makes a result field default to ``None`` when some environments lack it,
   and reports each such field so the build can write the availability table
   that ``is_available`` reads.

``AliasStrWrapperPlugin``
   Wraps input field aliases in ``str()`` so that editors type-check them.

Generated code says nothing about availability: ariadne-codegen warns at
codegen time for a deprecated selection, and the merge summary the build
prints lists what each environment lacks.
