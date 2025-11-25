Exceptions
==========

The GPP Client defines a hierarchy of exceptions to allow users to handle
failures in a predictable and structured way. All exceptions inherit from
:class:`~gpp_client.exceptions.GPPError`.

Most users will only need to catch high-level categories such as
:class:`~gpp_client.exceptions.GPPAuthError` or :class:`~gpp_client.exceptions.GPPNetworkError`. More advanced error handling can use
the full exception tree.

API Reference
-------------

.. automodule:: gpp_client.exceptions
   :members:
   :show-inheritance: