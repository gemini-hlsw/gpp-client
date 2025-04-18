Credentials
===========

The `GPPClient` supports multiple methods for authenticating with the GPP GraphQL API. This page describes how the client resolves credentials and how to configure them.

Credential Resolution Order
---------------------------

When creating a `GPPClient` instance, credentials are resolved in the following order:

1. **Direct constructor arguments**:

   If ``url`` and ``token`` are passed directly to `GPPClient`, they take precedence.

   .. code-block:: python

      from gpp_client import GPPClient

      client = GPPClient(
          url="https://gpp.example.org/graphql",
          token="your_token_here"
      )

2. **Environment variables**:

   If no arguments are passed, the client will check for:

   - ``GPP_URL``
   - ``GPP_TOKEN``

   These can be exported in your shell:

   .. code-block:: bash

      export GPP_URL="https://gpp.example.org/graphql"
      export GPP_TOKEN="your_token_here"

3. **TOML config file**:

   If no arguments and no environment variables are provided, the client will look for:

   .. code-block:: text

      ~/.gpp/config.toml

   Example content:

   .. code-block:: toml

      url = "https://gpp.example.org/graphql"
      token = "your_token_here"

If neither ``url`` nor ``token`` can be resolved from any source, a ``ValueError`` will be raised at runtime.

Configuration File Format
-------------------------

The config file must be located at:

.. code-block:: text

   ~/.gpp/config.toml

It should contain:

- ``url``: The full GPP GraphQL endpoint URL.
- ``token``: Your personal access token.

Example:

.. code-block:: toml

   url = "https://gpp.example.org/graphql"
   token = "abc123"
