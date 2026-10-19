Settings and environments
=========================

These classes hold what :doc:`guides/configuration` and
:doc:`guides/environments` describe: the settings a client resolves, the
environments it can reach, and their URLs.

Settings
--------

.. autoclass:: gpp_client.settings.GPPSettings
   :members:
   :show-inheritance:
   :exclude-members: model_config

.. autofunction:: gpp_client.settings.get_config_path

Environments
------------

.. autoclass:: gpp_client.environment.GPPEnvironment
   :members:
   :show-inheritance:

Endpoints
---------

.. autoclass:: gpp_client.urls.Endpoint
   :members:

.. automodule:: gpp_client.urls
   :members:
