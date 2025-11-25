Environment
===========

The :class:`~gpp_client.config.environment.GPPEnvironment` enum defines the
available GPP environments.

These environments correspond to distinct GPP deployments, each with its own:

- Base URL
- Token
- Configuration entry

Available Values
----------------

.. code-block:: python

   from gpp_client.config.environment import GPPEnvironment

   print(list(GPPEnvironment))

The enum contains:

- ``DEVELOPMENT``
- ``STAGING``
- ``PRODUCTION``

Usage
-----

The enum is used throughout the configuration system:

.. code-block:: python

   from gpp_client.config import GPPConfig, GPPEnvironment

   config = GPPConfig()
   config.activate(GPPEnvironment.STAGING)

String values are automatically normalized:

.. code-block:: python

   config.activate("development")   # valid
   config.activate("DEVELOPMENT")   # valid


Relationship to Defaults
------------------------

Each environment has a default URL defined in :doc:`defaults`.

The environment selected in the config file determines which token is used by
default.

API Reference
-------------

.. autoclass:: gpp_client.config.environment.GPPEnvironment
   :members:
   :undoc-members:
   :show-inheritance: