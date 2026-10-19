Generated exceptions
====================

The generated client defines these errors, and the client's own
:class:`~gpp_client.exceptions.GPPGraphQLError`,
:class:`~gpp_client.exceptions.GPPHttpError` and
:class:`~gpp_client.exceptions.GPPTransportError` inherit from them, so
``except GraphQLClientGraphQLMultiError`` still catches the errors GPP
returns. New code catches the ``gpp_client.exceptions`` classes. For when the
client raises each error, and what to do about it, see
:doc:`../guides/errors`.

API reference
-------------

.. automodule:: gpp_client.generated.exceptions
   :members:
