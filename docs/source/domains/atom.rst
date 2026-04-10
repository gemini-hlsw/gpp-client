Atom
====

The atom domain provides access to scheduler atom digest data.

Use :attr:`~gpp_client.GPPClient.atom` to request atom digests for one or more
observations.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      tsv = await client.atom.get_digests(
         observation_ids=["o-123", "o-456"]
      )


Getting Atom Digests
--------------------

Request atom digests as TSV data:

.. code-block:: python

   tsv = await client.atom.get_digests(
      observation_ids=["o-123"],
      accept_gzip=True,
   )

- Each observation ID is sent as a separate line in the request body
- The response is returned as a string (TSV format)

.. tip::

   Leave ``accept_gzip=True`` (default) for better performance on large responses.


Error Handling
--------------

- ``ValueError`` → invalid observation IDs
- ``aiohttp.ClientResponseError`` → authentication or HTTP errors


Notes
-----

This endpoint uses a REST API and may return compressed (gzip) responses.
Compression is handled automatically.


API Reference
-------------

.. autoclass:: gpp_client.domains.atom.AtomDomain
   :members:
   :exclude-members: __init__