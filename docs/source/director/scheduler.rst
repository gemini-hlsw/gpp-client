Scheduler
=========

The ``SchedulerDirector`` provides access to scheduler-related data in the GPP system by combining multiple underlying managers.

Its primary purpose is to retrieve programs along with their associated observation trees and metadata in a single call.

Usage Example
-------------

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import Director
   client = GPPClient()
   director = Director(client)
   programs = await director.scheduler.get_all()


.. automodule:: gpp_client.directors.scheduler
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:
