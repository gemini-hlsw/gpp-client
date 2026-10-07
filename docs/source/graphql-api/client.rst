Client
======

The ``client.graphql`` attribute is a
:class:`~gpp_client.generated.client.GraphQLClient` for the client's
environment. It has one method for each generated operation, plus ``query``,
``mutation`` and ``execute`` for custom documents. When a domain has the call
you need, use the domain instead.

API reference
-------------

.. autoclass:: gpp_client.generated.client.GraphQLClient
   :members:
