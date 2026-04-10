Program
=======

The program domain provides access to program queries, mutations, and
subscriptions.

Use :attr:`~gpp_client.GPPClient.program` to create, retrieve, update,
delete, restore, and subscribe to programs.

Quick Example
-------------

.. code-block:: python

   async with GPPClient() as client:
      program = await client.program.get_by_id("p-123")


Creating Programs
-----------------

Create a program:

.. code-block:: python

   result = await client.program.create(
      properties=properties,
      include_deleted=False,
   )

This method returns a generated GraphQL response model.


Retrieving Programs
-------------------

Get a program by ID:

.. code-block:: python

   result = await client.program.get_by_id("p-123")

Get a program by program reference:

.. code-block:: python

   result = await client.program.get_by_reference("GN-2026A-Q-1")

Get a program by proposal reference:

.. code-block:: python

   result = await client.program.get_by_proposal_reference("GN-2026A-Q-1")

Get multiple programs:

.. code-block:: python

   result = await client.program.get_all(
      include_deleted=False,
      where=where_input,
      limit=50,
   )


Updating Programs
-----------------

Update a single program by ID:

.. code-block:: python

   result = await client.program.update_by_id(
      "p-123",
      properties=properties,
      include_deleted=False,
   )

Update multiple programs:

.. code-block:: python

   result = await client.program.update_all(
      properties=properties,
      where=where_input,
      include_deleted=False,
   )


Delete and Restore
------------------

Delete a program by ID:

.. code-block:: python

   result = await client.program.delete_by_id("p-123")

Restore a program by ID:

.. code-block:: python

   result = await client.program.restore_by_id("p-123")


Subscriptions
-------------

Subscribe to program edit events:

.. code-block:: python

   async for event in client.program.subscribe_to_edits():
      print(event)

Restrict the subscription to a single program:

.. code-block:: python

   async for event in client.program.subscribe_to_edits(
      program_id="p-123"
   ):
      print(event)


Notes
-----

All program operations use GraphQL and return generated response models.

Subscription methods return asynchronous iterators.


API Reference
-------------

.. autoclass:: gpp_client.domains.program.ProgramDomain
   :members:
   :exclude-members: __init__