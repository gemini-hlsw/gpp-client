Code Generation
===============

The GPP Client uses `ariadne-codegen <https://github.com/mirumee/ariadne-codegen>`_ to generate the GraphQL transport client,
operations, models, enums, input types, fragments, and related API code.

All generated code lives in:

``src/gpp_client/generated/``

Running Codegen
---------------

Use the provided script:

.. code-block:: bash

   uv run --group codegen python scripts/run_codegen.py PRODUCTION

You may also generate code for the development environment:

.. code-block:: bash

   uv run --group codegen python scripts/run_codegen.py DEVELOPMENT

The environment argument is case-insensitive and must match a valid ``GPPEnvironment``.

What the Script Does
--------------------

The codegen script now uses an environment-specific Ariadne configuration file and performs the following steps:

1. Resolves the config file at:

   ``graphql/<environment>/ariadne-codegen.toml``

2. Runs ``ariadne-codegen`` using that config.

3. Loads the generated package settings from the TOML file.

4. Resolves the generated package directory from:

   - ``target_package_path``
   - ``target_package_name``

5. Writes a generated module named:

   ``package_environment.py``

   into the generated package so the packaged code knows which environment it was generated for.

Generated Package Environment
-----------------------------

After code generation completes, the script writes:

``src/gpp_client/generated/package_environment.py``

This module contains a package-level constant:

.. code-block:: python

   PACKAGE_ENVIRONMENT = "PRODUCTION"

or:

.. code-block:: python

   PACKAGE_ENVIRONMENT = "DEVELOPMENT"

This allows the generated package to retain knowledge of the environment it was built against.

Codegen Configuration
---------------------

Code generation is configured per environment using:

- ``graphql/development/ariadne-codegen.toml``
- ``graphql/production/ariadne-codegen.toml``

Custom Plugins
--------------

The project currently uses:

``custom_plugins.AliasStrWrapperPlugin``

This plugin corrects alias behavior for wrapped scalar types in the generated code.

Why Codegen Is Required
-----------------------

The GPP schema changes regularly. Those changes may introduce:

- New input types
- New enums
- New fields
- Updated nullability
- New operations
- New custom types

Rather than manually maintaining the generated GraphQL layer, the client regenerates it directly from the upstream schema.
