Scheduler
=========

The scheduler domain provides access to scheduler-specific program data.

Use :attr:`~gpp_client.GPPClient.scheduler` to query programs used by the
scheduler.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      programs = await client.scheduler.get_programs()


Programs
--------

Get scheduler programs:

.. code-block:: python

   result = await client.scheduler.get_programs()

Optionally filter by program IDs:

.. code-block:: python

   result = await client.scheduler.get_programs(
      programs_list=["p-123", "p-456"]
   )


Program IDs
-----------

Get all scheduler program IDs:

.. code-block:: python

   result = await client.scheduler.get_program_ids()


Notes
-----

All scheduler operations use GraphQL and return generated response models.


API Reference
-------------

.. autoclass:: gpp_client.domains.scheduler.SchedulerDomain
   :members:
   :undoc-members: