Target
======

The target domain provides access to target queries, mutations, and
subscriptions.

Use :attr:`~gpp_client.GPPClient.target` to create, retrieve, update, delete,
restore, clone, and subscribe to targets.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      target = await client.target.get_by_id(
         target_id="t-123",
         include_deleted=False,
      )


Creating Targets
----------------

Create a target by program ID:

.. code-block:: python

   result = await client.target.create_by_program_id(
      program_id="p-123",
      properties=properties,
      include_deleted=False,
   )

Create a target by program reference:

.. code-block:: python

   result = await client.target.create_by_program_reference(
      program_reference="GN-2026A-Q-1",
      properties=properties,
      include_deleted=False,
   )

Create a target by proposal reference:

.. code-block:: python

   result = await client.target.create_by_proposal_reference(
      proposal_reference="GN-2026A-Q-1",
      properties=properties,
      include_deleted=False,
   )


Retrieving Targets
------------------

Get a target by ID:

.. code-block:: python

   result = await client.target.get_by_id(
      target_id="t-123",
      include_deleted=False,
   )

Get multiple targets:

.. code-block:: python

   result = await client.target.get_all(
      include_deleted=False,
      where=where_input,
      limit=50,
   )


Updating Targets
----------------

Update a single target by ID:

.. code-block:: python

   result = await client.target.update_by_id(
      target_id="t-123",
      properties=properties,
      include_deleted=False,
   )

Update multiple targets:

.. code-block:: python

   result = await client.target.update_all(
      properties=properties,
      include_deleted=False,
      where=where_input,
      limit=25,
   )


Cloning Targets
---------------

Clone a target:

.. code-block:: python

   result = await client.target.clone(
      target_id="t-123",
      include_deleted=False,
      properties=properties,
      replace_in=["o-123", "o-456"],
   )

The optional ``replace_in`` argument may be used to replace the cloned target
in one or more observations.


Delete and Restore
------------------

Delete a target by ID:

.. code-block:: python

   result = await client.target.delete_by_id(target_id="t-123")

Restore a target by ID:

.. code-block:: python

   result = await client.target.restore_by_id(target_id="t-123")


Subscriptions
-------------

Subscribe to target edit events:

.. code-block:: python

   async for event in client.target.subscribe_edits():
      print(event)

Restrict the subscription to a single target:

.. code-block:: python

   async for event in client.target.subscribe_edits(
      target_id="t-123"
   ):
      print(event)


Notes
-----

All target operations use GraphQL and return generated response models.

Subscription methods return asynchronous iterators.


API Reference
-------------

.. autoclass:: gpp_client.domains.target.TargetDomain
   :members:
   :exclude-members: __init__