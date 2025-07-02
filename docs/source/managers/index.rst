Managers
========

This section documents the resource-specific manager classes available on the ``GPPClient``.

Overview
--------

A **manager** encapsulates all interaction logic for a specific GraphQL resource such as `programs`, `observations`, `targets`, and more. Each manager provides an asynchronous, Pythonic interface to the underlying GraphQL schema.

All managers inherit from a shared :doc:`BaseManager <base>`, and most compose lightweight mixins for common operations like ``create``, ``update_all``, ``get_by_id``, and ``delete_by_id``.

Accessing Managers
------------------

Each manager is exposed as an attribute on the ``GPPClient`` instance:

.. code-block:: python

   from gpp_client import GPPClient

   client = GPPClient()

   # Fetch a program by ID
   program = await client.program.get_by_id("p-123")


Responsibilities
----------------

Managers handle:

- Asynchronous GraphQL query/mutation execution
- Structured GraphQL field selection
- Enforcement of resource-specific rules (e.g. requiring one program reference)

Manager Patterns
----------------

Most managers follow this pattern:

- ``create()`` accepts a generated input model and builds a typed mutation
- ``get_all()`` provides filterable and paginated queries
- ``get_by_id()`` accepts an identifier or reference and returns the resource
- ``update_all()`` performs batch updates to all matching resources.
- ``update_by_id()`` supports targeted updates using partial input models
- ``delete_by_id()`` deletes an item
- ``restore_by_id()`` restores a deleted item

API Reference
-------------

.. toctree::
   :maxdepth: 1

   base
   call-for-proposals
   program
   program-note
   target
   observation
   site-status
