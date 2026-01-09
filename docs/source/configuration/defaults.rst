Defaults
========

The :mod:`gpp_client.config.defaults` module defines all built-in default values
for the GPP Client configuration system.

These defaults include:

- The default configuration file name
- The application directory used for storage
- The default GPP environment
- The mapping of environments to GraphQL URLs
- The names of supported environment variables for tokens

Configuration File Naming
-------------------------

The default configuration file is always named:

``config.toml``

This file is stored in a directory determined by
:func:`typer.get_app_dir`, based on:

``GPPDefaults.app_name`` → ``"gpp-client"``

Environment Defaults
--------------------

The default environment is:

``PRODUCTION``

See :doc:`environment` for all supported environments.

Environment Variable Names
--------------------------

Each environment has a dedicated variable name for its token:

- ``GPP_DEVELOPMENT_TOKEN``
- ``GPP_STAGING_TOKEN``
- ``GPP_PRODUCTION_TOKEN``

These names live in:

``GPPDefaults.env_var_env_tokens``

.. note::

   Whether these environment variables are *used* depends on the user's config
   file. See :doc:`config`.

API Reference
-------------

.. autoclass:: gpp_client.config.defaults._GPPDefaults
   :members:
   :show-inheritance:
   :no-index: