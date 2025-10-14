GOATS
=====

The ``GOATSDirector`` exposes **coordinator** objects that orchestrate
several *managers* to satisfy GOATS-specific workflows.

Usage Example
-------------

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import Director
   client = GPPClient()
   director = Director(client)
   observations = await director.goats.observation.get_all()


.. automodule:: gpp_client.directors.goats
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Coordinator Layer
-----------------

.. automodule:: gpp_client.directors.goats.coordinators.observation
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. automodule:: gpp_client.directors.goats.coordinators.program
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance: