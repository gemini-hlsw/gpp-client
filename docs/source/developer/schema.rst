Schema Management
=================

The GPP Client depends on the GPP GraphQL schema. Schema files must stay current
so generated models, enums, input types, and operations match the target GPP
environment.

Downloading a Schema
--------------------

Use the schema download script with a target environment:

.. code-block:: bash

   uv run --group schema python scripts/download_schema.py DEVELOPMENT

or:

.. code-block:: bash

   uv run --group schema python scripts/download_schema.py PRODUCTION

The environment argument is case-insensitive and must match a valid
``GPPEnvironment``.

Schema Configuration
--------------------

The script uses environment-specific Ariadne Codegen schema configuration files:

.. code-block:: text

   graphql/schemas/development.toml
   graphql/schemas/production.toml

Each TOML file defines how the schema is downloaded and where it is written.

Authentication
--------------

The required token depends on the selected environment:

.. list-table::
   :header-rows: 1

   * - Environment
     - Required token
   * - ``DEVELOPMENT``
     - ``GPP_DEVELOPMENT_TOKEN``
   * - ``PRODUCTION``
     - ``GPP_TOKEN``

If the required token is not set, the script exits before attempting to download
the schema.

Generated Schema Files
----------------------

Downloaded schemas are written according to the matching Ariadne Codegen schema
configuration.

After downloading a schema, regenerate the client code if the schema changed.