GPP Client Documentation
========================

The GPP Client is an asynchronous Python client for interacting with the
Gemini Program Platform (GPP).

It provides:

- A high-level domain-based interface for GPP resources.
- Automatic environment-aware authentication and configuration.
- Generated GraphQL models for advanced/custom API interactions.
- Built-in CLI tooling for common tasks.

Quick Start
-----------

Install the package:

.. code-block:: bash

   pip install gpp-client

Configure your authentication token:

.. code-block:: bash

   export GPP_TOKEN=...

Create a client and fetch data:

.. code-block:: python

   from gpp_client import GPPClient

   async with GPPClient() as client:
      program = await client.program.get_by_id("p-123")

Documentation Overview
----------------------

Use the **User Guide** for learning standard library usage, the
**API Reference** for detailed technical documentation, and the
**Developer Guide** for contributing or maintaining the project.

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   client
   configuration
   cli/index
   domains/index
   exceptions


.. toctree::
   :maxdepth: 2
   :caption: API Reference

   graphql-api/index
   rest-client
   environment


.. toctree::
   :maxdepth: 2
   :caption: Developer Guide

   developer/setup
   developer/schema
   developer/codegen
   developer/workflow
   developer/documentation
   developer/pull-requests
   developer/releases
   contributing