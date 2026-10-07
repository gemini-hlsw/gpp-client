Exceptions
==========

The ``gpp_client.exceptions`` module holds the client's own errors and
warnings. Every error inherits from :class:`~gpp_client.exceptions.GPPError`.
:class:`~gpp_client.exceptions.GPPFieldLeavingWarning` is a warning, not an
error.

Errors that GPP returns for a GraphQL call are
:doc:`graphql-api/exceptions` instead. For when the client raises each error,
and what to do about it, see :doc:`guides/errors`.

.. automodule:: gpp_client.exceptions
   :members:
   :show-inheritance:
