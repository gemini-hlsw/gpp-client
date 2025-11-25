Configuration
=============

The GPP Client stores user-specific settings in a local TOML file. This includes:

- The active GPP environment
- API tokens for each environment
- A flag that controls whether OS environment variables may be used

The configuration system is composed of three layers:

1. :doc:`config` — the high-level interface used by the client and CLI
2. :doc:`defaults` — built-in default values (paths, filenames, baseline environment)
3. :doc:`environment` — the :class:`~gpp_client.config.environment.GPPEnvironment` enum
4. :doc:`models` — Pydantic models representing the configuration file

This section documents each of these pieces in detail.

.. note::

   The *resolution* of credentials (how URLs/tokens are chosen at runtime) is
   covered separately in :doc:`../credentials`.

.. toctree::
   :maxdepth: 1
   :caption: Contents

   config
   defaults
   environment
   models