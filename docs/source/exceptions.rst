Exceptions
==========

The ``gpp_client.exceptions`` module holds every error the client raises.
Every error inherits from :class:`~gpp_client.exceptions.GPPError`.

The errors GPP answers with also inherit from the generated
:doc:`graphql-api/exceptions`. For when the client raises each error, and
what to do about it, see :doc:`guides/errors`.

.. automodule:: gpp_client.exceptions
   :members:
   :show-inheritance:
