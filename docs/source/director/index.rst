Director
========

This section documents how to interact with multiple managers to satisfy the specific needs of a service.

Overview
--------

A **director** allows interaction with more than one manager through a unified interface.
This is necessary because the ODB is limited in the amount of information it can retrieve at once.
To reconstruct more complex structures, the system must issue multiple queries to different managers.

Service-specific directors are organized under distinct namespaces and use the regular client to perform queries and mutations.

Using a Specific Director
-------------------------

The director interface allows you to select a specific director by namespace for each service.


.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import GPPDirector
   client = GPPClient()
   director = GPPDirector(client)
   programs = await director.scheduler.program.get_all()


Or from the console:


.. code-block:: bash

   gpp sched program list


.. automodule:: gpp_client.director
   :members:
   :undoc-members:
   :inherited-members:
   :show-inheritance:


API Reference
-------------

.. toctree::
   :maxdepth: 1

   base
   scheduler
   goats
