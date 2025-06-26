Directors Interface
===================

This section documents the included way to interact with more than one manager to satisfy the specific needs for a service.

Overview
--------

A **director** allows to interact with more than one manager but using the same interface the managers do to ask for specific elements.
This is because the ODB is limited on the information it can bring when working with too much information so it needs to be breakdown in multiple queries from different managers to recreate more complex structures.

Service-specific directors are all under an specific namespace in **Director** and uses the regular client for specific query/mutations.

Use an specific director
------------------------

The director interface allows to select an specific director using the namespace for each service.

.. code-block:: python

   from gpp_client import GPPClient
   from gpp_client import Director


   client = GPPClient()
   director = Director(client)
   programs = await director.scheduler.program.get_all()
