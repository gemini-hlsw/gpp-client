Site Status
===========

The site status domain provides access to current Gemini North and Gemini South
status information.

Use :attr:`~gpp_client.GPPClient.site_status` to retrieve observatory status,
available instruments, shutter state, and GMOS configuration details.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      status = await client.site_status.get_by_id("north")


Getting Site Status
-------------------

Get status for Gemini North:

.. code-block:: python

   status = await client.site_status.get_by_id("north")

Get status for Gemini South:

.. code-block:: python

   status = await client.site_status.get_by_id("south")

The returned payload includes:

- Site name
- Status validity timestamp
- Availability summary
- Available instruments
- Comment
- Shutter state
- GMOS configuration details


Returned Data
-------------

The returned dictionary contains keys such as:

- ``site``
- ``validity``
- ``available``
- ``instruments``
- ``comment``
- ``shutter``
- ``gmos_config``

Example:

.. code-block:: python

   status = await client.site_status.get_by_id("north")
   print(status["site"])
   print(status["shutter"])


API Reference
-------------

.. autoclass:: gpp_client.domains.site_status.SiteStatusDomain
   :members:
   :undoc-members: