Follow changes as they happen
=============================

A subscription keeps a connection open to GPP and yields an event each time
the data you follow changes.

Follow edits
------------

Subscription methods are ``async`` generators, so you loop over them with
``async for``. This example waits until someone edits an observation in the
program, prints the edit, and stops:

.. code-block:: python

   edits = client.observation.subscribe_to_edits(
       program_id="p-10a",
   )
   async for event in edits:
       edit = event.observation_edit
       print(edit.edit_type, edit.observation_id)
       break
   # EditType.UPDATED o-1a2

Without ``break``, the loop runs until GPP closes the connection. A normal
close ends the loop quietly, but a network failure raises
``websockets.exceptions.ConnectionClosedError``. To keep following, catch that
error and subscribe again.
For the errors a subscription can raise when it starts, see
:doc:`errors`.

Stop after a while
------------------

To stop after a while, wrap the loop in ``asyncio.timeout``:

.. code-block:: python

   import asyncio

   edits = client.observation.subscribe_to_edits(
       program_id="p-10a",
   )
   try:
       async with asyncio.timeout(60):
           async for event in edits:
               edit = event.observation_edit
               print(edit.observation_id)
   except TimeoutError:
       print("No more edits for now.")

Other subscriptions
-------------------

Domains that offer subscriptions name their methods ``subscribe_...``, such
as ``client.target.subscribe_edits`` and
``client.scheduler.subscribe_to_calculation_updates``. For every domain, see
:doc:`../domains/index`. The ``client.graphql`` attribute also has a method for
every GraphQL subscription that GPP offers.

Before it connects, the client checks the subscription against the selected
environment, as it does for queries. For details, see
:ref:`environment-errors`.
