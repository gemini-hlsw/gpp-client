GOATS
=====

The GOATS domain provides access to GOATS-specific data exposed through GraphQL.

Use :attr:`~gpp_client.GPPClient.goats` to retrieve programs and observations
used within GOATS workflows.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      programs = await client.goats.get_programs()


Programs
--------

Get all GOATS programs:

.. code-block:: python

   result = await client.goats.get_programs()


Observations
------------

Get GOATS observations for a program:

.. code-block:: python

   result = await client.goats.get_observations_by_program_id("p-123")


Notes
-----

All GOATS operations use GraphQL and return generated response models.

Refer to the generated types for the full response structure.


API Reference
-------------

.. autoclass:: gpp_client.domains.goats.GOATSDomain
   :members:
   :exclude-members: __init__