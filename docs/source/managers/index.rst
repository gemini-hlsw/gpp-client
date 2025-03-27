Manager Modules
===============

This section documents the resource managers that power the `GPPClient`.

Overview
--------

In this library, a **Manager** is a high-level interface to a specific GraphQL resource, such as program notes, proposals, or observations. Managers are responsible for:

- Registering and executing resource-specific GraphQL queries and mutations
- Composing reusable mixins that implement common operations (create, get, update, delete, restore)
- Optionally overriding logic to simplify the interface

.. note::

   All managers inherit from a shared :doc:`BaseManager <base_manager>`, which encapsulates core functionality.

Every manager is available as an attribute of the `GPPClient`:

.. code-block:: python

    client = GPPClient(...)
    notes = await client.program_note.get_batch(...)
    proposal = await client.proposal.get_by_id("p-123")

Why Managers?
-------------

Managers serve as a consistent and extensible namespace for operations on GraphQL resources. Rather than scattering query logic across the codebase, each resource has a dedicated manager that:

- Provides a focused, intuitive interface
- Follows async/await patterns for modern Python
- Enables custom overrides for ergonomic method signatures
- Supports field selection overrides for GraphQL payload optimization

Example: `ProgramNoteManager`
-----------------------------

The `ProgramNoteManager` demonstrates the power of this pattern. It combines several mixins to support:

- Creating new program notes
- Fetching them by ID or in batches
- Updating and deleting notes
- Auto-generating `set_values` payloads for mutations

Custom logic in `create()` and `update_by_id()` builds structured mutation payloads automatically, making it easier for users.

API Reference
-------------

.. toctree::
   :maxdepth: 1

   base_manager
   program_note
