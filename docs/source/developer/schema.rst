Schema Management
=================

The GPP Client depends directly on the GPP GraphQL schema. Maintaining an up-to-date
local schema is essential for running ``ariadne-codegen`` and generating correct
client code.

Schema Download Script
----------------------

Use the provided script to download a schema for any environment:

.. code-block:: bash

   uv run python scripts/download_schema.py PRODUCTION

The script handles:

- Reading the correct token from the environment
- Validating that the environment is known
- Downloading via ``gql-cli``
- Writing the resulting schema to ``schemas/<env>.schema.graphql``

Required Environment Variables
------------------------------

Tokens must be provided through the environment. The expected variables are:

- ``GPP_DEVELOPMENT_TOKEN``
- ``GPP_STAGING_TOKEN``
- ``GPP_PRODUCTION_TOKEN``

Only the token for the selected environment is required.

Example:

.. code-block:: bash

   export GPP_PRODUCTION_TOKEN="abc123"

.. note::

   Tokens *must* be provided via environment variables. They are not read from
   the :class:`gpp_client.config.GPPClient` configuration file during schema download.

Directory Layout
----------------

Downloaded schemas live in:

``schemas/<environment>.schema.graphql``

These files are committed to the repository.