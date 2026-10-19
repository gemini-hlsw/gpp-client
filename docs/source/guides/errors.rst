Handle errors
=============

Every error the client raises inherits from ``GPPError``, so one ``except``
catches them all. Catch the specific error first, then the broader ones:

.. code-block:: python

   from gpp_client.exceptions import (
       GPPError,
       GPPGraphQLError,
       GPPHttpError,
       NotAvailable,
   )

   try:
       await client.program.get_by_id("p-10a")
   except NotAvailable as error:
       print(error)
   except GPPGraphQLError as error:
       for problem in error.errors:
           print("GPP error:", problem.message)
   except GPPHttpError as error:
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
   * - :class:`~gpp_client.exceptions.NotAvailable`
     - The selected environment lacks the operation the call needs. Nothing is sent.
     - Follow the message. For details, see :ref:`environment-errors`.
   * - :class:`~gpp_client.exceptions.GPPValidationError`
     - The client rejects your input before it sends a change. For example, an upload gets both ``file_path=`` and ``content=``, or you ask for a workflow state the observation can't move to.
     - Fix the input.
   * - :class:`~gpp_client.exceptions.GPPRetryableError`
     - ``workflow_state.update_by_id`` finds GPP still calculating the observation.
     - Try again later, or call ``update_by_id_with_retry``, which retries for you.
   * - :class:`~gpp_client.exceptions.GPPClientError`
     - Something else fails on the client side. For example, the environment name is unknown, a download would overwrite a file, or an attachment call can't connect.
     - Read the message.
   * - :class:`~gpp_client.exceptions.GPPGraphQLError`
     - GPP returns errors for a GraphQL call or subscription, from a domain or from ``client.graphql``. When GPP also returned data, ``data`` holds it.
     - Read each item of ``errors``. For what the message tells you, see :ref:`server-errors`.
   * - :class:`~gpp_client.exceptions.GPPHttpError`
     - GPP returns an HTTP error status for a GraphQL call, an attachment upload, download, update or delete, or an atom digest or scheduler visibility-change request. A 404 on an attachment call means the attachment doesn't exist; on the atom and scheduler paths it means the environment may not serve the path.
     - Read ``status_code``.
   * - :class:`~gpp_client.exceptions.GPPTransportError`
     - GPP can't be reached, a call times out, a subscription's connection drops or is refused, or GPP sends something that isn't GraphQL. ``__cause__`` holds the HTTP or websocket library's own error.
     - Try again later.
   * - ``httpx.RequestError``
     - ``client.site_status`` can't connect, or times out.
     - Try again later.
   * - ``httpx.HTTPStatusError``
     - ``client.site_status`` gets an HTTP error from gemini.edu.
     - Try again later.
   * - ``ValueError``
     - ``download_by_id`` gets a ``save_to=`` that is a file, or a scheduler method gets a ``page_size`` below 2.
     - Fix the input.

The errors GPP answers with, ``GPPGraphQLError``, ``GPPHttpError`` and
``GPPTransportError``, also inherit from the generated
:class:`~gpp_client.generated.exceptions.GraphQLClientError` classes, so code
that catches those keeps working. For every error class, see
:doc:`../exceptions`.

.. _server-errors:

Errors GPP answers with
-----------------------

The client sends every call as the selected environment receives it and lets
GPP judge the input. When GPP rejects a call, the error message names the
environment, for example:

.. code-block:: text

   GPP production returned errors: Field 'sequence' is not defined by type
   'CloneObservationInput'.

GPP doesn't know the field on that environment. Either you sent an input that
this environment doesn't take, such as a development-only field on
production, or your install is behind the server. For the first, leave the
field unset, or select the other environment with
``GPPClient(environment="development")`` or ``GPP_ENVIRONMENT=development``.
For the second, upgrade.

The same error on a different environment often means a different thing, so
check which environment the message names before you change your code.

.. _environment-errors:

Calls the environment can't take
--------------------------------

Development gets GPP changes first, so the two environments differ.
``client.is_available`` and ``client.enum_values`` say what the selected
environment has (see :ref:`fields-the-environment-lacks`).

Before it sends a generated operation, the client looks up the copy of that
operation for the selected environment. When the environment lacks the
operation entirely, the client raises
:class:`~gpp_client.exceptions.NotAvailable` and sends nothing:

.. code-block:: text

   The operation getDraft is not available on production. It is available on
   development. Nothing was sent.

The error carries the same facts as attributes that your code can test:
``item``, ``environment`` and ``available``.

A scheduler or atom REST call goes out as written. When the environment
doesn't serve the path, GPP answers 404 and the client raises
``GPPHttpError`` with ``status_code`` 404; the message names the environment
and adds that the path may not be served on that environment.

Everything else goes to GPP as written: a development-only input field on
production, a custom query, a document passed to ``client.graphql.execute``.
If the environment can't take it, GPP answers with the error described in
:ref:`server-errors`.

Fields the selected environment lacks
-------------------------------------

When a domain method or a generated ``client.graphql`` method selects a result
field that the selected environment doesn't have, the client leaves that field
out of the call, and the field is ``None`` in the result. So check for ``None``
before you use such a field, or ask ``client.is_available``, as
:ref:`fields-the-environment-lacks` shows. A custom query or an ``execute``
document that selects such a field goes to GPP as written, and GPP answers
with an error.

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
