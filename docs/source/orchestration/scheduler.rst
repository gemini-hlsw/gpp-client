Scheduler
=========

The ``SchedulerDirector`` exposes **coordinator** objects that orchestrate
several *managers* to satisfy Scheduler-specific workflows.

Usage Example
-------------

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import Director
   client = GPPClient()
   director = Director(client)
   programs = await director.scheduler.program.get_all()


.. automodule:: gpp_client.directors.scheduler
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Coordinator Layer
-----------------

Each coordinator bundles related manager calls into a single, domain-focused API.  For example, ``ProgramCoordinator`` combines ``ProgramManager`` and ``ObservationManager`` to return a program plus its observation hierarchy in one asynchronous method.

.. automodule:: gpp_client.directors.scheduler.coordinators.program
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Subscriber Integration
----------------------

The ``ProgramCoordinator`` for the Scheduler Director currently includes a ``subscribe_to`` attribute that provides
access to subscription functionality for testing purposes. This allows you to subscribe
to real-time program edits and updates directly through the Scheduler Director.

.. note::

   The subscriber is currently integrated into the Scheduler Director for testing.
   In future releases, the subscriber architecture may be restructured.

Usage Example
~~~~~~~~~~~~~

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import Director

   client = GPPClient()
   director = Director(client)

   # Access the subscriber through the program coordinator
   subscriber = director.scheduler.program.subscribe_to

   # Subscribe to program edits
   async for edit in await subscriber.get_edits(program_id="p-123"):
       print(f"Received edit: {edit}")

Available Methods
~~~~~~~~~~~~~~~~~

- ``get_edits(program_id: str | None)``: Subscribe to edits for a specific program.
  Returns an async iterator of program edit changes.
- ``get_calculations_updates(program_id: str | None)``: Subscribe to calculations updates for a specific program.
  Returns an async iterator of program calculations updates. This is only for te Observation Coordinator.
