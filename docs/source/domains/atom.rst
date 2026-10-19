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

- ``GPPHttpError`` when GPP rejects the observation IDs, when the selected
  environment doesn't serve atom digests (404), or for other HTTP errors,
  such as a token without access. ``status_code`` tells which.
- ``GPPTransportError`` when it can't connect.

Each is a ``GPPError`` and names the environment. For more, see
:doc:`../guides/errors`.

API reference
-------------

.. autoclass:: gpp_client.domains.atom.AtomDomain
   :members:
   :undoc-members:
