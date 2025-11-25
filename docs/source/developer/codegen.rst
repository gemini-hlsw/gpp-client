Code Generation
===============

The GPP Client uses `ariadne-codegen <https://github.com/mirumee/ariadne-codegen>`_ to generate all GraphQL models, enums,
inputs, fragments, and the underlying ``_GPPClient`` transport layer.

All generated code lives in:

``src/gpp_client/api/``

Running Codegen
---------------

Use the provided script:

.. code-block:: bash

   uv run python scripts/run_codegen.py PRODUCTION

This script:

1. Validates that the schema exists.
2. Writes a temporary ``codegen.toml`` based on project defaults.
3. Creates a backup of the existing ``src/gpp_client/api`` directory.
4. Runs ``ariadne-codegen``.
5. Restores the backup on failure.
6. Deletes the backup on success.

Codegen Configuration
---------------------

The configuration is constructed dynamically, but corresponds to:

.. code-block:: toml

   [tool.ariadne-codegen]
   schema_path = "schemas/production.schema.graphql"
   query_path = "src/queries"
   target_package_path = "src/gpp_client"
   target_package_name = "api"
   convert_to_snake_case = true
   enable_custom_operations = true
   client_name = "_GPPClient"
   client_file_name = "_client"
   plugins = ["custom_plugins.AliasStrWrapperPlugin"]

This produces:

``src/gpp_client/api/``

Custom Plugins
--------------

The project currently uses:

``custom_plugins.AliasStrWrapperPlugin``

This plugin corrects how certain scalar wrappers behave with aliases.

Why Codegen Is Required
-----------------------

The GPP schema changes regularly. Each change may add:

- New input types
- New enums
- New fields
- Updated nullability
- New custom types

Rather than maintain all Pydantic models manually, the project regenerates them
using the upstream schema.

.. note::

   The GPP Client itself is intentionally *thin*. Most logic resides in resource
   managers and higher-level abstractions. The generated code is not intended to
   contain business logic except for the defined queries, mutations, and subscriptions.