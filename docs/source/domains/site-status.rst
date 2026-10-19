Site status
===========

The ``client.site_status`` domain reads the status of Gemini North or Gemini
South from the public status pages on gemini.edu. It doesn't call GPP, but the
client still needs a token to start.

To read a site's status, pass ``"north"`` or ``"south"`` to ``get_by_id``:

.. code-block:: python

   status = await client.site_status.get_by_id("north")
   print(status["site"])
   # Gemini North
   shutter = status["shutter"]
   if shutter is not None:
       print(shutter["state"], shutter["timestamp"])

The result is a dictionary with the keys ``site``, ``validity``,
``available``, ``instruments``, ``comment``, ``shutter`` and ``gmos_config``.

The ``shutter`` value is ``None`` when the page shows no shutter status.
Otherwise it's a dictionary with these keys:

- ``state`` - the first word of the page's shutter text, in lower case.
- ``timestamp`` - the time in that text, if there is one.
- ``raw_string`` - the text itself.

API reference
-------------

.. autoclass:: gpp_client.domains.site_status.SiteStatusDomain
   :members:
   :undoc-members:
