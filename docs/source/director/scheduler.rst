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

Coordinator layer
-----------------

Each coordinator bundles related manager calls into a single, domain-focused API.  For example, ``ProgramCoordinator`` combines ``ProgramManager`` and ``ObservationManager`` to return a program plus its observation hierarchy in one asynchronous method.

.. automodule:: gpp_client.directors.scheduler.coordinators.program
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance: