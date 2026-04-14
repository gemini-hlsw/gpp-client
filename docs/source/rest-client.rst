REST Client
===========

The REST client provides low-level access to non-GraphQL endpoints used by the
GPP client.

It manages authenticated HTTP sessions and provides the underlying transport
layer for REST-based operations.

.. warning::

   This is considered advanced functionality and is rarely needed directly.

Most users should prefer using the domain interfaces exposed through
:class:`~gpp_client.GPPClient`.

API Reference
-------------

.. autoclass:: gpp_client.rest.RESTClient
   :members:
   :show-inheritance: