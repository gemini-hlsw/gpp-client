Credentials
===========

The GPP Client supports multiple sources for authentication. This page explains
how the client determines *which* token and *which* environment to use at
runtime.

Most users only need to set a token once, either through environment variables or
via the configuration file. Advanced configuration options are documented in
:doc:`configuration/config`.

Overview
--------

Credential resolution is performed by
:class:`~gpp_client.credentials.CredentialResolver`. The resolver determines:

- Which **environment** to use
- Which **token** to use
- The correct **GraphQL URL** for that environment

The resolution follows a strict priority order.

Resolution Priority
-------------------

The following table summarizes how credentials are resolved, highest priority
first:

1. **Explicit arguments** passed to :class:`~gpp_client.GPPClient`
2. **Environment variables** (if enabled in config)
3. **Configuration file** stored on disk

If no valid token can be found, a :class:`~gpp_client.exceptions.GPPAuthError`
is raised.

Priority 1: Explicit Arguments
------------------------------

The highest priority is arguments provided directly when constructing the
client.

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import GPPEnvironment

   client = GPPClient(env=GPPEnvironment.STAGING, token="abc123")

If ``env`` or ``token`` is provided explicitly, they override all other sources.

Priority 2: Environment Variables
---------------------------------

If explicit arguments are not provided and environment variables are **enabled**
(see ``disable_env_vars`` in the configuration file), the resolver checks for:

Environment selector:

- ``GPP_ENV``

Token variables (per environment):

- ``GPP_DEVELOPMENT_TOKEN``
- ``GPP_STAGING_TOKEN``
- ``GPP_PRODUCTION_TOKEN``

Generic fallback token:

- ``GPP_TOKEN``

Examples:

.. code-block:: bash

   export GPP_ENV="STAGING"
   export GPP_STAGING_TOKEN="staging-token-value"

When these are present, they override the configuration file.

Priority 3: Local Configuration File
------------------------------------

If neither explicit arguments nor environment variables provide credentials, the
resolver uses the local configuration file managed by
:class:`~gpp_client.config.GPPConfig`.

Location:

- POSIX: ``~/.gpp-client/config.toml``
- Windows: ``%APPDATA%/GPP Client/config.toml``

Example:

.. code-block:: toml

   env = "PRODUCTION"
   disable_env_vars = false

   [tokens]
   DEVELOPMENT = ""
   STAGING = ""
   PRODUCTION = "my-prod-token"

Disabling Environment Variables
-------------------------------

Users may disable the use of environment variables entirely:

.. code-block:: python

   from gpp_client import GPPConfig

   config = GPPConfig()
   config.disable_env_vars(save=True)

When disabled, the resolver will *skip* all environment variable lookups.

Full Resolution Example
-----------------------

.. code-block:: python

   from gpp_client.credentials import CredentialResolver

   url, token, env = CredentialResolver.resolve()

   print(env)     # GPPEnvironment.PRODUCTION
   print(url)     # default production GraphQL URL
   print(token)   # token resolved from args/env/config

Internals
---------

The credential system uses two internal helper components:

Environment Variable Reader
---------------------------

.. autoclass:: gpp_client.credentials.env_var_reader.EnvVarReader
   :members:
   :show-inheritance:

Credential Resolver
-------------------

.. autoclass:: gpp_client.credentials.CredentialResolver
   :members:
   :show-inheritance:

Notes
-----

- Most users will interact with credentials through the CLI or configuration
  page.
- Advanced users may override environments programmatically using
  ``env=...``.
- Detailed configuration options are described in :doc:`configuration/config`.