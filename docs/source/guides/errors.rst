Handle errors
=============

The client's own errors inherit from ``GPPError``. Errors that GPP returns for
a GraphQL call, and some REST errors, don't. So catch the specific error
first, then the broader ones:

.. code-block:: python

   from gpp_client.exceptions import (
       GPPEnvironmentError,
       GPPError,
   )
   from gpp_client.generated.exceptions import (
       GraphQLClientGraphQLMultiError,
       GraphQLClientHttpError,
   )

   try:
       await client.program.get_by_id("p-10a")
   except GPPEnvironmentError as error:
       print(error)
   except GraphQLClientGraphQLMultiError as error:
       for problem in error.errors:
           print("GPP error:", problem.message)
   except GraphQLClientHttpError as error:
       print("HTTP error:", error.status_code)
   except GPPError as error:
       print("Client error:", error)

What can go wrong
-----------------

This table lists each error, when the client raises it, and what to do. Each
linked name opens the error's reference entry, which lists its attributes.

.. list-table::
   :header-rows: 1
   :widths: 30 45 25

   * - Error
     - Raised when
     - What to do
   * - :class:`~gpp_client.exceptions.GPPAuthError`
     - You build a client and the selected environment has no token.
     - Set the variable the message names, or pass ``token=``.
   * - :class:`~gpp_client.exceptions.GPPEnvironmentError`
     - The call doesn't fit the selected environment.
     - Follow the message. For details, see :ref:`environment-errors`.
   * - :class:`~gpp_client.exceptions.GPPValidationError`
     - The client rejects your input before it sends a change. For example, an upload gets both ``file_path=`` and ``content=``, or you ask for a workflow state the observation can't move to.
     - Fix the input.
   * - :class:`~gpp_client.exceptions.GPPRetryableError`
     - ``workflow_state.update_by_id`` finds GPP still calculating the observation.
     - Try again later, or call ``update_by_id_with_retry``, which retries for you.
   * - :class:`~gpp_client.exceptions.GPPResponseError`
     - GPP refuses an attachment upload, download, update or delete.
     - Read ``status_code`` and ``message``.
   * - :class:`~gpp_client.exceptions.GPPClientError`
     - Something else fails on the client side. For example, the environment name is unknown, a download would overwrite a file, or an attachment call can't connect.
     - Read the message.
   * - :class:`~gpp_client.generated.exceptions.GraphQLClientGraphQLMultiError`
     - GPP returns errors for a GraphQL call or subscription, from a domain or from ``client.graphql``.
     - Read each item of ``errors``.
   * - :class:`~gpp_client.generated.exceptions.GraphQLClientInvalidResponseError`
     - GPP's response to a GraphQL call isn't JSON, or holds neither data nor errors.
     - Try again later.
   * - :class:`~gpp_client.generated.exceptions.GraphQLClientHttpError`
     - GPP returns an HTTP error for a GraphQL call.
     - Read ``status_code``.
   * - ``aiohttp.ClientResponseError``
     - An atom digest or scheduler visibility-change request gets an HTTP error.
     - Read ``status`` and ``message``.
   * - ``aiohttp.ClientError``
     - An atom digest or scheduler visibility-change request can't connect.
     - Try again later.
   * - ``httpx.RequestError``
     - A GraphQL call or ``client.site_status`` can't connect, or times out. The error is a subclass, such as ``httpx.ConnectError`` or ``httpx.TimeoutException``.
     - Try again later.
   * - ``httpx.HTTPStatusError``
     - ``client.site_status`` gets an HTTP error from gemini.edu.
     - Try again later.
   * - ``OSError``
     - A subscription can't connect.
     - Try again later.
   * - ``websockets.exceptions.InvalidHandshake``
     - The server refuses to open a subscription's connection.
     - Read the message, then subscribe again.
   * - :class:`~gpp_client.generated.exceptions.GraphQLClientError`
     - GPP doesn't acknowledge a new subscription in time, or sends a message the client can't read.
     - Subscribe again.
   * - ``websockets.exceptions.ConnectionClosedError``
     - An open subscription's connection drops.
     - Subscribe again.
   * - ``ValueError``
     - GPP rejects the observation IDs sent for atom digests, ``download_by_id`` gets a ``save_to=`` that is a file, or a scheduler method gets a ``page_size`` below 2.
     - Fix the input.

The ``GraphQLClient...`` errors live in ``gpp_client.generated.exceptions``,
and they all inherit from :class:`~gpp_client.generated.exceptions.GraphQLClientError`.
For every error class, see :doc:`../exceptions` and
:doc:`../graphql-api/exceptions`.

.. _environment-errors:

Calls the environment can't take
--------------------------------

Development gets GPP changes first, so the two environments differ. The
:doc:`../graphql-api/input-types` and :doc:`../graphql-api/enums` reference
pages mark what only one environment has.

Before it sends a call, the client checks the call against the selected
environment. That includes subscriptions, custom queries and documents passed
to ``client.graphql.execute``. In two cases, the client raises
:class:`~gpp_client.exceptions.GPPEnvironmentError` and sends nothing:

- The call uses an operation, field, argument, input field, or enum value that
  the environment doesn't have.
- The call leaves unset an argument or input field that the environment
  requires.

The error message says what to change, for example:

.. code-block:: text

   The input field CloneObservationInput.sequence is not available on
   production. It is available on development. Leave it unset on production,
   or select development with GPPClient(environment="development") or
   GPP_ENVIRONMENT=development. Nothing was sent.

The client raises the error even when every environment rejects the call, as
long as another environment has the item that the selected one lacks. For
example, a call might set both a field and the field that replaces it. In that
case, ``available`` lists the environments that have the item, and the message
doesn't suggest selecting one of them, because the call would fail there too.

If no environment has the item, such as a misspelled field, the client can't
blame the environment. So it sends the call as it is, and GPP reports the
mistake.

The error also carries the same facts as attributes that your code can test,
such as ``kind`` and ``available``. For each attribute, see
:class:`~gpp_client.exceptions.GPPEnvironmentError`.

A scheduler or atom call that the environment doesn't serve also raises
``GPPEnvironmentError``, with ``kind`` set to ``EnvironmentItemKind.REST_PATH``.
The client only finds this out after the request, so ``available`` is empty.

Fields the selected environment lacks
-------------------------------------

When a domain method or a generated ``client.graphql`` method selects a result
field that the selected environment doesn't have, the client leaves that field
out of the call, and the field is ``None`` in the result. So check for ``None``
before you use such a field. A custom query or an ``execute`` document that
selects such a field raises ``GPPEnvironmentError`` instead.

Fields about to leave production
--------------------------------

On production, the client issues a
:class:`~gpp_client.exceptions.GPPFieldLeavingWarning`, once per field,
when you select a field that development has already removed. The warning is
a ``FutureWarning``, and its ``field`` attribute names the field
(``Type.field``). Expect that field to leave production soon.

To fail fast in your tests, turn the warning into an error:

.. code-block:: python

   import warnings

   from gpp_client.exceptions import (
       GPPFieldLeavingWarning,
   )

   warnings.simplefilter(
       "error", GPPFieldLeavingWarning
   )

.. _unknown-enum-values:

Enum values added after your release
------------------------------------

GPP can add an enum value after your release was built. A result that holds
such a value still parses: the value becomes a member of the enum, and its
``value`` is the raw string. The member equals no member your release knows,
as this example shows:

.. code-block:: python

   from gpp_client.generated.enums import (
       ProposalStatus,
   )

   status = ProposalStatus("STATUS_ADDED_LATER")
   print(status.value)
   # STATUS_ADDED_LATER
   print(status == ProposalStatus.ACCEPTED)
   # False

If your code branches on an enum, give it a fallback branch for values it
doesn't know.
