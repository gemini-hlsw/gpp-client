Environment
===========

This section documents environment and endpoint helpers used by the GPP client
to resolve runtime environments and service URLs.

These APIs support client configuration and endpoint selection.

Environment Configuration
-------------------------

The environment configuration defines the supported runtime environments for
the GPP client.

.. autoclass:: gpp_client.environment.GPPEnvironment
   :members:
   :show-inheritance:


Endpoint Utilities
------------------

The endpoint utilities provide helper functions for resolving GraphQL and
WebSocket URLs for a given environment.

.. autoclass:: gpp_client.urls.Endpoint
   :members:

.. automodule:: gpp_client.urls
   :members: