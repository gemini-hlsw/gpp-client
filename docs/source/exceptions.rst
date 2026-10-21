Exceptions
==========

The GPP Client defines a hierarchy of exceptions to allow users to handle
failures in a predictable and structured way. All exceptions inherit from
:class:`~gpp_client.exceptions.GPPError`.

Most users only need to catch high-level categories such as
:class:`~gpp_client.exceptions.GPPAuthError` or
:class:`~gpp_client.exceptions.GPPServerError`. More advanced error handling
can use the full exception tree.

Every :class:`~gpp_client.exceptions.GPPServerError` names the environment the
request went to, so a request sent to the wrong environment reads differently
from a request with wrong data. When GPP rejects a request, the
:class:`~gpp_client.exceptions.GPPHttpError` carries GPP's own messages, the
commit that GPP runs, and the commit that the client's schema was downloaded
at. If the two commits differ, the client may be behind the server, and
upgrading it is the first thing to try.

API Reference
-------------

.. automodule:: gpp_client.exceptions
   :members:
   :show-inheritance: