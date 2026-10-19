.. _updating-the-schema:

Update the schema
=================

GPP changes its GraphQL schema almost every day. A schema update brings the
committed schemas up to date, rebuilds the client from them, and runs the
tests. One command does all of it. For what the build does at each step, see
:doc:`how-the-client-is-built`.

1. Run the update
-----------------

Run the update from the repository root:

.. code-block:: bash

   uv run --group codegen python -m scripts.schema_update

The command asks each environment for its schema by introspection, which asks
the server to describe its schema. It writes the schemas that changed to
``src/gpp_client/schemas/<environment>.graphql``, rebuilds the generated
client, and then runs the test suite. You don't need a token. If a server
refuses anonymous introspection, the command names the token variable to set.

Running the command twice without a change in GPP changes nothing, so you can
rerun it whenever you want to be sure that the checkout is current.

When an environment answers with a schema that doesn't build, the command
keeps that environment's committed schema, updates the other environment, and
says so in its output. That's a problem in GPP, not in the client. Run the
update again later, and keep the held line for the release notes, which
:doc:`releases` describes.

The command ends with three Markdown summaries, which you paste into the pull
request body:

- The schema update summary says, for each environment, whether its schema
  changed, stayed the same, or was held.
- The merge summary lists the types that the merge renamed to development's
  name, the fields whose type differs between the environments, the type names
  that mean a different kind of type on each environment, and the renames the
  merge refused because the evidence was ambiguous. A renamed union or
  interface gets a warning line: production answers ``__typename`` with its
  own name, which the client does not map, so that rename is the trigger to
  add a ``__typename`` map.
- The trim summary lists, for each environment, the operations that the
  environment can't run and what the build removed from the operations it
  receives: fields, arguments, parts of input literals, fragments, and
  variables left unused.

Between the build and the summaries, the command prints ariadne-codegen's
deprecation warnings. Each one names a deprecated field that the operations or
the generated input types still use.

Each downloaded schema starts with ``# schema-date: YYYY-MM-DD``, the day of
the download, so a reader of the file knows how current it is. When GPP's
schema hasn't changed, the update keeps the committed file and its date.

To see what changed in the schemas themselves, compare them with the last
commit:

.. code-block:: bash

   git diff src/gpp_client/schemas/

To download or build on their own, for example to try an operation change
against schemas you already have, the two steps are still separate commands:

.. code-block:: bash

   uv run --group schema python -m scripts.download_schema
   uv run --group codegen python -m scripts.build_client

2. Fix a failed build
---------------------

The build stops at the first problem and prints what it found. The message
names the operation, field, or environment. The downloaded schemas stay in
place, so after you fix the cause, rerun the update.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Message contains
     - What to do
   * - ``Schema files not found``
     - Run the update again.
   * - ``Merged schema is invalid``
     - The schemas can't be merged. This is a problem in GPP, not in the
       client. Report it to the GPP team and restore the previous schemas
       with ``git checkout src/gpp_client/schemas/`` until it's fixed.
   * - ``Operations select what no environment has``
     - The list names each operation or fragment and the field, argument,
       type, or value that no environment has any more. Change the operation
       to use what replaced it, or remove the selection.
   * - ``Codegen failed``
     - An operation breaks another GraphQL rule, such as an unused variable
       or a duplicate name. The message says which.
   * - ``Trimmed operations are invalid``
     - An operation trimmed for one environment breaks a GraphQL rule there,
       for example a variable declared nullable where that environment
       requires it, or a required input field only that environment has.
       Change the operation; the build never changes a variable's type.
   * - ``did not get a None default`` or ``Reading gql(...) queries back``
     - This is a bug in the build, not in your change. Report it.

A difference between the environments never fails the build. Where a field,
argument, or input field has a different type on each environment, the
generated client takes production's type and the merge summary lists the
conflict. Where a type name means a different kind of type on each environment,
production's definition wins, and the summary lists what the build dropped
from development's schema because of it. Where production still uses an old
name for an input type or enum, the summary lists the rename and the alias
that the generated code carries for the old name.

3. Fix a failed test
--------------------

The update runs ``pytest`` on the rebuilt client and reports whether it
passed. Run the remaining checks yourself:

.. code-block:: bash

   uv run ruff check . && uv run ruff format --check .
   uv run ty check --error-on-warning src/gpp_client

When ty reports an unknown attribute or import in ``src/gpp_client/domains/``,
GPP renamed or removed what that domain calls. Change the domain method to the
new generated name. If the field is gone, remove what uses it and say so in the
pull request.

A failing test in ``tests/docs/`` names a page and a line, where an example
uses a name that changed. Fix the example.

4. Open the pull request
------------------------

Commit everything that the update changed, in one commit:

- ``src/gpp_client/schemas/``
- ``src/gpp_client/generated/``
- any operation you edited in ``graphql/operations/``

Paste the three summaries from the update into the pull request body, with any
new deprecation warnings. Say which operations you changed and why.
