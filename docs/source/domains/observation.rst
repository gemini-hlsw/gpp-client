Observation
===========

The observation domain provides access to observation queries, mutations, and
subscriptions.

Use :attr:`~gpp_client.GPPClient.observation` to create, retrieve, update,
delete, restore, clone, and subscribe to observations.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      observation = await client.observation.get_by_id("o-123")


Creating and Cloning
--------------------

Create an observation:

.. code-block:: python

   result = await client.observation.create(input=create_input)

Clone an observation:

.. code-block:: python

   result = await client.observation.clone(input=clone_input)

Both methods return generated GraphQL response models.


Retrieving Observations
-----------------------

Get a single observation by ID:

.. code-block:: python

   result = await client.observation.get_by_id("o-123")

Get a single observation by reference:

.. code-block:: python

   result = await client.observation.get_by_reference("GN-2026A-Q-1-1")

Get multiple observations:

.. code-block:: python

   result = await client.observation.get_all(
      include_deleted=False,
      where=where_input,
      limit=50,
   )


Updating Observations
---------------------

Update a single observation by ID:

.. code-block:: python

   result = await client.observation.update_by_id(
      "o-123",
      properties=properties,
   )

Update a single observation by reference:

.. code-block:: python

   result = await client.observation.update_by_reference(
      "GN-2026A-Q-1-1",
      properties=properties,
   )

Update multiple observations:

.. code-block:: python

   result = await client.observation.update_all(input=bulk_update_input)


Delete and Restore
------------------

Delete an observation by ID:

.. code-block:: python

   result = await client.observation.delete_by_id("o-123")

Delete an observation by reference:

.. code-block:: python

   result = await client.observation.delete_by_reference("GN-2026A-Q-1-1")

Restore an observation by ID:

.. code-block:: python

   result = await client.observation.restore_by_id("o-123")

Restore an observation by reference:

.. code-block:: python

   result = await client.observation.restore_by_reference("GN-2026A-Q-1-1")


Subscriptions
-------------

Subscribe to observation edit events:

.. code-block:: python

   async for event in client.observation.subscribe_to_edits():
      print(event)

Restrict the subscription to a program:

.. code-block:: python

   async for event in client.observation.subscribe_to_edits(
      program_id="p-123"
   ):
      print(event)

Subscribe to observation calculation updates:

.. code-block:: python

   async for event in client.observation.subscribe_to_calculation_updates():
      print(event)


Notes
-----

All observation operations use GraphQL and return generated response models.

Subscription methods return asynchronous iterators.


API Reference
-------------

.. autoclass:: gpp_client.domains.observation.ObservationDomain
   :members:
   :undoc-members: