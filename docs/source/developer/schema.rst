Schema Management
=================

The GPP Client depends directly on the GPP GraphQL schema. Keeping the local schema files current is required for
successful code generation and to ensure the generated client matches the target GPP environment.

Schema Download Script
----------------------

Use the provided script to download the schema for a specific environment:

.. code-block:: bash

   uv run --group schema python scripts/download_schema.py PRODUCTION

You may also download the development schema:

.. code-block:: bash

   uv run --group schema python scripts/download_schema.py DEVELOPMENT

The environment argument is case-insensitive and must match a valid ``GPPEnvironment``.

What the Script Does
--------------------

The schema download script performs the following steps:

1. Validates the requested environment.
2. Loads settings using ``GPPSettings(environment_override=env)``.
3. Resolves the correct authentication token for that environment.
4. Resolves the GraphQL endpoint using ``get_graphql_url(...)``.
5. Downloads the schema using ``gql-cli``.
6. Writes the schema to the environment-specific GraphQL directory.

Downloaded Schema Location
--------------------------

Schemas are written to:

``graphql/<environment>/schema.graphql``

For example:

- ``graphql/development/schema.graphql``
- ``graphql/production/schema.graphql``

These schema files are used by the corresponding environment-specific
``ariadne-codegen.toml`` files.

Authentication and Credentials
------------------------------

The schema download script uses ``GPPSettings`` to resolve credentials for the selected environment.

Supported token settings include:

- ``GPP_TOKEN``
- ``GPP_DEVELOPMENT_TOKEN``

Credential resolution follows the normal settings system, including:

- Environment variables
- A local ``.env`` file
- The app TOML configuration file

See the :ref:`configuration` page for full details on credential configuration.

Token resolution is environment-aware:

- ``DEVELOPMENT`` uses ``GPP_DEVELOPMENT_TOKEN``
- ``PRODUCTION`` uses ``GPP_TOKEN``

If the required token for the selected environment cannot be resolved, the script exits with an authentication error.
