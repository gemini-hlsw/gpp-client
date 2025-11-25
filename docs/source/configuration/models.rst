Models
======

.. note::

   End users typically **do not need to interact with these models directly**.
   They are internal building blocks used by :class:`~gpp_client.config.GPPConfig`
   to validate, load, and serialize the configuration file.
   You will rarely (if ever) instantiate these models manually.

The GPP Client uses Pydantic models to validate and serialize the contents of
the configuration file. These models ensure:

- Consistent schema validation
- Automatic empty-string cleanup
- Correct serialization back to TOML or JSON

Tokens Model
------------

:class:`~gpp_client.config.models.Tokens` stores API tokens for each defined environment.

Empty strings in the TOML file are automatically converted to ``None`` during
validation.

.. code-block:: python

   from gpp_client.config.models import Tokens

   tokens = Tokens(DEVELOPMENT="abc", STAGING="")
   print(tokens.STAGING)   # → None

When serializing back to TOML or JSON, ``None`` becomes an empty string.

ConfigFile Model
----------------

:class:`~gpp_client.config.models.ConfigFile` represents the full configuration file.

Fields include:

- ``env`` — active environment
- ``disable_env_vars`` — whether environment vars are used
- ``tokens`` — the environment token container

Example file:

.. code-block:: toml

   env = "PRODUCTION"
   disable_env_vars = false

   [tokens]
   DEVELOPMENT = ""
   STAGING = "staging-token"
   PRODUCTION = "prod-token"


Interaction With GPPConfig
--------------------------

The :class:`~gpp_client.config.GPPConfig` class wraps this model and provides:

- File I/O
- Token/Env mutation helpers
- Runtime convenience methods

See :doc:`config` for the operational interface.

API Reference
-------------

.. autoclass:: gpp_client.config.models.Tokens
   :members:

.. autoclass:: gpp_client.config.models.ConfigFile
   :members:
   :show-inheritance: