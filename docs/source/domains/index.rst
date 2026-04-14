Domains
=======

Domains provide the primary resource-oriented interface for interacting with GPP.

Each domain groups operations for a specific area of the API, such as programs,
observations, targets, attachments, or workflow state.

Domains are accessed from :class:`~gpp_client.GPPClient`:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient() as client:
      program = await client.program.get_by_id("p-123")
      observation = await client.observation.get_by_id("o-456")

In most cases, domains should be preferred over direct use of the underlying
GraphQL or REST clients.

Design
------

Domains provide a stable, resource-oriented interface over generated GraphQL
operations and supporting REST endpoints.

Depending on the resource, a domain may use:

- GraphQL only
- REST only
- Both GraphQL and REST

.. tip::

   Use domains for routine operations. Access the underlying clients only for
   advanced workflows.

Available Domains
-----------------

The following domains are available from :class:`~gpp_client.GPPClient`:

- :attr:`~gpp_client.GPPClient.scheduler`
- :attr:`~gpp_client.GPPClient.program`
- :attr:`~gpp_client.GPPClient.observation`
- :attr:`~gpp_client.GPPClient.target`
- :attr:`~gpp_client.GPPClient.workflow_state`
- :attr:`~gpp_client.GPPClient.atom`
- :attr:`~gpp_client.GPPClient.attachment`
- :attr:`~gpp_client.GPPClient.goats`
- :attr:`~gpp_client.GPPClient.site_status`

Domain Guides
-------------

.. toctree::
   :maxdepth: 1

   attachment
   atom
   goats
   scheduler
   observation
   program
   target
   site-status
   workflow-state