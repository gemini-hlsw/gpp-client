Config
======

The :class:`~gpp_client.config.GPPConfig` class manages the local configuration file
used by the GPP Client. It supports:

- Loading and validating TOML configuration data
- Storing per-environment API tokens
- Selecting and activating environments
- Disabling or enabling the use of OS environment variables
- Exporting the configuration as TOML, JSON, or Python dictionaries

The configuration file is validated using Pydantic models.
For details on the underlying schema, see :doc:`models`.

Configuration File Location
---------------------------

The configuration file is stored in the system-appropriate application data
directory:

- POSIX: ``~/.config/gpp-client/config.toml``
- Windows: ``%APPDATA%/gpp-client/config.toml``

This path is determined by :func:`typer.get_app_dir` and the defaults defined in
:mod:`gpp_client.config.defaults`.

For details on the default paths and filenames, see :doc:`defaults`.

Configuration Structure
-----------------------

The configuration file is a TOML document validated against the
:class:`~gpp_client.config.models.ConfigFile` model.

Example:

.. code-block:: toml

   env = "PRODUCTION"
   disable_env_vars = false

   [tokens]
   PRODUCTION = "prod-token"
   DEVELOPMENT = "dev-token"
   STAGING = "test-token"

Environment Selection
---------------------

``GPPConfig`` tracks the *active environment*, which determines which token
``GPPClient`` uses unless overridden explicitly.

Tokens may be stored for all environments, but only one environment is active at
a time.

For details on available environments and rules, see :doc:`environment`.

Loading and Saving
------------------

Configuration is loaded automatically on creation:

.. code-block:: python

   config = GPPConfig()
   print(config.active_env)

Changes may be saved explicitly:

.. code-block:: python

   config.save()

Token Management
----------------

Store a token:

.. code-block:: python

   config.set_token("DEVELOPMENT", "dev-token", save=True)

Clear a token:

.. code-block:: python

   config.clear_token("STAGING", save=True)

Clear all tokens:

.. code-block:: python

   config.clear_tokens(save=True)

Environment Activation
----------------------

The active environment determines which token is used by default:

.. code-block:: python

   config.activate("PRODUCTION", save=True)
   print(config.active_env)

Combined operation:

.. code-block:: python

   config.set_credentials("DEVELOPMENT", "xyz", activate=True, save=True)


Environment Variable Control
----------------------------

Users may disable OS environment variables entirely:

.. code-block:: python

   config.disable_env_vars(save=True)

Or re-enable them:

.. code-block:: python

   config.enable_env_vars(save=True)

.. note::

   Disabling environment variables affects credential resolution.
   For details, see :doc:`../credentials`.

Exporting Configuration
-----------------------

For debugging or automation purposes:

.. code-block:: python

   config.to_dict()
   config.to_json()
   config.to_toml()


Creating a Default Configuration File
-------------------------------------

.. code-block:: python

   GPPConfig.create_default_config_file()

This writes an empty, validated configuration with default values.

API Reference
-------------

.. autoclass:: gpp_client.config.GPPConfig
   :members:
   :undoc-members:
   :show-inheritance: