Manager Modules
===============

This section documents the resource-specific manager classes available on the ``GPPClient``.

Overview
--------

A **manager** encapsulates all interaction logic for a specific GraphQL resource such as `programs`, `observations`, `targets`, and more. Each manager provides an asynchronous, Pythonic interface to the underlying GraphQL schema.

All managers inherit from a shared :doc:`BaseManager <base_manager>`, and most compose lightweight mixins for common operations like ``create``, ``update_all``, ``get-by-id``, and ``soft-deletion``.

Accessing Managers
------------------

Each manager is exposed as an attribute on the ``GPPClient`` instance:

.. code-block:: python

   from gpp_client import GPPClient

   client = GPPClient()

   # Fetch a program by ID
   program = await client.program.get_by_id("p-2025A-001")

   # Create a new program note
   note = await client.program_note.create(
       properties=ProgramNotePropertiesInput(
           title="Important update",
           text="Please confirm new calibration procedures.",
           is_private=False
       ),
       program_id="p-2025A-001"
   )

Responsibilities
----------------

Managers handle:

- Asynchronous GraphQL query/mutation execution
- Payload building using ``ariadne-codegen`` input types
- Structured GraphQL field selection
- Soft-delete and restore operations
- Enforcement of resource-specific rules (e.g. requiring one program reference)

Manager Patterns
----------------

Most managers follow this pattern:

- ``create()`` accepts a generated input model and builds a typed mutation
- ``get_all()`` provides filterable and paginated queries
- ``get_by_id()`` accepts an identifier or reference and returns the resource
- ``update_all()`` performs batch updates to all matching resources.
- ``update_by_id()`` supports targeted updates using partial input models
- ``delete_by_id()`` and ``restore_by_id()`` toggle resource existence

API Reference
-------------

.. toctree::
   :maxdepth: 1

   base_manager
   call_for_proposals
   program
   program_note
   target
   observation