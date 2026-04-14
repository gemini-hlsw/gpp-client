Client
======

The primary entry point for interacting with the GPP API.

The :class:`~gpp_client.GPPClient` provides:

- Authenticated GraphQL and REST clients
- Environment-aware configuration
- Access to domain-specific interfaces for GPP resources


Quick Example
-------------

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient() as client:
      programs = await client.program.get_all()


Overview
--------

The client initializes:

- A GraphQL client for generated operations
- A REST client for non-GraphQL endpoints
- Domain interfaces for working with GPP resources

Each resource is accessed through a domain:

.. code-block:: python

   await client.program.get_by_id("p-123")
   await client.observation.get_by_id("o-456")


.. note::

   All domain methods are asynchronous and must be used within an event loop.


Authentication
--------------

Authentication is resolved automatically based on the active environment.

- Development environment → requires ``GPP_DEVELOPMENT_TOKEN``
- Production environment → requires ``GPP_TOKEN``

.. code-block:: bash

   export GPP_DEVELOPMENT_TOKEN=...
   export GPP_TOKEN=...

You may also pass a token explicitly:

.. code-block:: python

   client = GPPClient(token="my-token")

.. note::

   The provided token is applied to the active environment automatically.


Creating a Client
-----------------

Basic usage:

.. code-block:: python

   client = GPPClient()

Enable debug logging:

.. code-block:: python

   client = GPPClient(debug=True)

The client will automatically resolve:

- The correct API endpoints
- The appropriate authentication token


Available Domains
-----------------

The following domains are available:

- :attr:`~gpp_client.GPPClient.scheduler`
- :attr:`~gpp_client.GPPClient.program`
- :attr:`~gpp_client.GPPClient.observation`
- :attr:`~gpp_client.GPPClient.target`
- :attr:`~gpp_client.GPPClient.workflow_state`
- :attr:`~gpp_client.GPPClient.atom`
- :attr:`~gpp_client.GPPClient.attachment`
- :attr:`~gpp_client.GPPClient.goats`
- :attr:`~gpp_client.GPPClient.site_status`

Each domain provides operations specific to its resource.


Connectivity
------------

Use :meth:`~gpp_client.GPPClient.ping` to verify connectivity and authentication:

.. code-block:: python

   ok, error = await client.ping()

   if ok:
      print("Connected")
   else:
      print("Failed:", error)


Lifecycle Management
--------------------

The client manages network resources and should be closed when no longer needed.

.. code-block:: python

   await client.close()

The client also supports async context management:

.. code-block:: python

   async with GPPClient() as client:
      ...


Underlying Clients
------------------

Advanced users may access the underlying transport clients directly.

GraphQL Client
^^^^^^^^^^^^^^

The generated GraphQL client is available via:

- :attr:`~gpp_client.GPPClient.graphql`

REST Client
^^^^^^^^^^^

The REST client is available via:

- :attr:`~gpp_client.GPPClient.rest`

.. warning::

   Direct use of the REST client is considered advanced usage and is rarely
   necessary. Prefer using domain interfaces whenever possible.


API Reference
-------------

.. autoclass:: gpp_client.GPPClient
   :members:
   :show-inheritance: