.. _updating-the-schema:

Update the schema
=================

GPP changes its GraphQL schema almost every day. A schema update brings the
committed schemas up to date and rebuilds the client from them. For what the
build does at each step, see :doc:`how-the-client-is-built`.

1. Download the schemas
-----------------------

This command downloads the development and production schemas:

.. code-block:: bash

   uv run --group schema python -m scripts.download_schema

The script downloads each schema by introspection, which asks the server to
describe its schema, and writes it to
``graphql/schemas/<environment>.graphql``. To download only some environments,
name them:

.. code-block:: bash

   uv run --group schema python -m scripts.download_schema production

You don't need a token. If a server refuses, the script names the token
variable to set.

To see what changed, compare the schemas with the last commit:

.. code-block:: bash

   git diff graphql/schemas/

2. Build the client
-------------------

Rebuild the client from the new schemas:

.. code-block:: bash

   uv run --group codegen python -m scripts.build_client

The build needs no token and no network. It prints ariadne-codegen deprecation
warnings, and each one names a deprecated field that the operations or the
generated input types still use. The build ends with a trim summary. For each
environment, the summary lists the operations that the environment can't run,
and what the build removed from the operations it receives.

3. Fix a failed build
---------------------

The build stops at the first problem and prints what it found. The message
names the operation, field, or environment.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Message contains
     - What to do
   * - ``Schema files not found``
     - Run the download again.
   * - ``Schema of <environment> is invalid``,
       ``Type '<name>' has a different kind on two environments`` or
       ``Merged schema is invalid``
     - The schemas can't be merged. This is a problem in GPP, not in the
       client. Report it to the GPP team and keep the previous schemas until
       it's fixed.
   * - ``Operations select fields whose type differs between environments``
     - Remove the named field from the operation in ``graphql/operations/``
       until the environments agree.
   * - ``Operations could not be read``
     - An operation file isn't valid GraphQL. Fix the error that the message
       names.
   * - ``Codegen failed``
     - Most often, an operation uses something that no environment has any
       more. Change the operation to use what replaced it, or remove it.
   * - ``Trimmed operations are invalid``
     - An operation trimmed for one environment breaks a GraphQL rule there,
       for example with an inline input field that the environment lacks. Pass
       the value as a variable instead, or change the operation.
   * - ``did not get a None default``, ``the trimmed lookup cannot find``, or
       ``Reading gql(...) queries back``
     - This is a bug in the build, not in your change. Report it.

The build can also print the warning ``Left out <field>: type differs``. That
warning is fine as long as no operation selects the field.

4. Check the result
-------------------

Run the checks and the tests:

.. code-block:: bash

   uv run ruff check . && uv run ruff format --check .
   uv run ty check --error-on-warning src/gpp_client
   uv run pytest
   uv run python -m scripts.check_environment_independence

When ty reports an unknown attribute or import in ``src/gpp_client/domains/``,
GPP renamed or removed what that domain calls. Change the domain method to the
new generated name. If the field is gone, remove what uses it and say so in the
pull request.

A failing test in ``tests/docs/`` names a page and a line, where an example
uses a name that changed. Fix the example.

5. Open the pull request
------------------------

Commit everything that the download and the build changed, in one commit:

- ``graphql/schemas/``
- ``src/gpp_client/generated/``
- ``llms.txt``
- any operation you edited in ``graphql/operations/``

Paste the trim summary from the build into the pull request body, with any
``Left out`` warnings and new deprecation warnings. Say which operations you
changed and why.
