Configuration
=============

The ``GPPConfig`` class manages the loading, saving, and updating of the local GPP Client configuration file.

It provides an interface for reading and modifying credentials (GraphQL URL and token) as well as other future configuration options such as CLI preferences.

Overview
--------

The configuration file is stored in the appropriate system application data directory:

- On POSIX systems: ``~/.gpp-client/config.toml``
- On Windows systems: ``C:\Users\<username>\AppData\Roaming\GPP Client\config.toml``

The configuration file is stored in TOML format and typically includes:

.. code-block:: toml

   [credentials]
   url = "https://your-url-here.com"
   token = "your_token_here"

.. note::

   For more information on how credentials are resolved, see :doc:`credentials`.

Usage
-----

Typical usage involves instantiating the class, retrieving credentials, or updating them:

.. code-block:: python

   from gpp_client.config import GPPConfig

   config = GPPConfig()

   # Get credentials.
   url, token = config.get_credentials()

   # Update credentials and save.
   config.set_credentials(url="https://your-url-here.com", token="your_token_here")

Important Behaviors
--------------------

- When saving, the necessary parent directories are created automatically if they do not exist.
- After writing to disk, the internal configuration data is reloaded to ensure consistency.
- Missing configuration files are treated as empty configurations rather than raising errors.

API Reference
-------------

.. autoclass:: gpp_client.config.GPPConfig
   :members:
   :undoc-members:
   :show-inheritance:


