Configuration
=============

Overview
--------

The client uses ``pydantic-settings`` to resolve configuration at runtime.

Configuration is:

- Environment-aware
- Strictly validated
- Resolved from multiple sources


Environment Model
-----------------

The active environment is determined by the installed package:

- Development builds → development environment
- Production builds → production environment

The environment cannot be changed at runtime.

.. note::

   The ``environment_override`` option exists for internal tooling
   (e.g., code generation) and should not be used in normal client usage.


Authentication
--------------

Authentication is environment-specific.

- Development requires ``GPP_DEVELOPMENT_TOKEN``
- Production requires ``GPP_TOKEN``

.. code-block:: bash

   export GPP_DEVELOPMENT_TOKEN=...
   export GPP_TOKEN=...

An explicit token may also be provided when creating the client:

.. code-block:: python

   client = GPPClient(token="my-token")

The token is applied to the active environment.

.. note::

   When passing ``token=`` explicitly:

   - In development builds, the token is used as ``development_token``
   - In production builds, the token is used as ``token``

   This allows the same code to work across environments without modification.

.. warning::

   Tokens are not interchangeable. A development client will **not**
   use ``GPP_TOKEN`` and will fail if ``GPP_DEVELOPMENT_TOKEN`` is not set.


Configuration Sources
---------------------

Settings are resolved using the following precedence:

1. Initialization parameters
2. Environment variables
3. ``.env`` file
4. Application config file
5. Model defaults

Each field is resolved independently.

.. tip::

   Different fields may come from different sources. For example:

   - ``token`` from environment variables
   - ``debug`` from a TOML config file


Configuration File
------------------

An optional TOML configuration file may be used.

The directory is determined using :func:`typer.get_app_dir` and follows
platform-specific conventions.

Typical locations:

- macOS:
  ``~/Library/Application Support/<App Name>``
- Linux:
  ``~/.config/<app-name>``
- Windows:
  ``C:\Users\<user>\AppData\Roaming\<App Name>``

The full path is:

.. code-block:: text

   <app-dir>/<config-file-name>

Example:

.. code-block:: text

   ~/.config/gpp-client/settings.toml

The file is only used if it exists.

Example contents:

.. code-block:: toml

   token = "prod-token"
   development_token = "dev-token"
   debug = true

.. tip::

   To see the exact path used on your system:

   .. code-block:: python

      from gpp_client.settings import get_config_path
      print(get_config_path())


API Reference
-------------

.. autoclass:: gpp_client.settings.GPPSettings
   :members:
   :show-inheritance:
   :exclude-members: model_config