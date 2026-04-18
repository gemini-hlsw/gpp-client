Code Generation
===============

The GPP Client uses `ariadne-codegen <https://github.com/mirumee/ariadne-codegen>`_
to generate the GraphQL transport client, operations, models, enums, input types,
fragments, and related API code.

All generated code lives in:

``src/gpp_client/generated/``


GraphQL Operations Structure
----------------------------

GraphQL operations are organized to support both shared and environment-specific behavior.

Directory layout:

- ``graphql/operations/shared/``
  Contains operations and fragments used in both development and production.

- ``graphql/operations/development_only.graphql``
  Contains operations and fragments that exist only in the development schema.

Behavior:

- **Production**
  Uses only ``shared/``.

- **Development**
  Uses ``shared/`` + ``development_only.graphql``.

During code generation, these are assembled into a temporary build directory
and passed to ``ariadne-codegen``.

Rules:

- ``development_only.graphql`` must be **additive only**.
- Operation and fragment names must not collide with anything in ``shared/``.
- Violations will fail code generation.
- Empty or missing ``development_only.graphql`` is ignored.

Guidelines:

- Use ``shared/`` for stable operations supported in both environments.
- Use ``development_only.graphql`` for experimental or unreleased schema usage.
- When promoting operations to production, move them into ``shared/``.


Running Codegen
---------------

Use the provided script:

.. code-block:: bash

   uv run --group codegen python scripts/run_codegen.py PRODUCTION

Or for development:

.. code-block:: bash

   uv run --group codegen python scripts/run_codegen.py DEVELOPMENT

The environment argument is case-insensitive and must match a valid ``GPPEnvironment``.


What the Script Does
--------------------

The codegen script performs the following steps:

1. Resolves the config file at:

   ``graphql/codegen/<environment>.toml``

2. Assembles GraphQL operations:

   - Copies ``shared/`` into a temporary build directory.
   - Adds ``development_only.graphql`` for development.

3. Cleans previous artifacts:

   - Removes the ``build/`` directory.
   - Removes the generated package directory.

4. Runs ``ariadne-codegen``.

5. Writes a generated module:

   ``package_environment.py``

   into the generated package.


Generated Package Environment
-----------------------------

After code generation completes, the script writes:

``src/gpp_client/generated/package_environment.py``

This module contains:

.. code-block:: python

   PACKAGE_ENVIRONMENT = "PRODUCTION"

or:

.. code-block:: python

   PACKAGE_ENVIRONMENT = "DEVELOPMENT"

This allows the generated package to retain knowledge of the environment it was built against.


Codegen Configuration
---------------------

Code generation is configured per environment:

- ``graphql/codegen/development.toml``
- ``graphql/codegen/production.toml``


Custom Plugins
--------------

The project currently uses:

``custom_plugins.AliasStrWrapperPlugin``

This plugin corrects alias behavior for wrapped scalar types in the generated code.


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