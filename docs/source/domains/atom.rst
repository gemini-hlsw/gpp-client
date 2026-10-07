Atom
====

The ``client.atom`` domain fetches atom digests for the scheduler. Its
``get_digests`` method returns them as one string of tab-separated values, with
one row per line:

.. code-block:: python

   tsv = await client.atom.get_digests(
       observation_ids=["o-1a2", "o-1a3"],
   )
   for line in tsv.splitlines():
       print(line.split("\t"))

The ``get_digests`` method can raise these errors:

- ``ValueError`` when GPP rejects the observation IDs.
- ``GPPEnvironmentError`` when the selected environment doesn't serve atom
  digests.
- ``aiohttp.ClientResponseError`` for other HTTP errors, such as a token
  without access.
- ``aiohttp.ClientError`` when it can't connect.

Only ``GPPEnvironmentError`` is a ``GPPError``. For more, see
:doc:`../guides/errors`.

API reference
-------------

.. autoclass:: gpp_client.domains.atom.AtomDomain
   :members:
   :undoc-members:
