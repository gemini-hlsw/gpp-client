GPP GraphQL Client Building Blocks
==================================

This section documents the auto-generated modules created from the GPP GraphQL schema via ``ariadne-codegen``. These modules form the foundation for all client interactions with the GPP API, and are used extensively when constructing GraphQL inputs and parsing responses.

- **Input types**: Used to construct payloads for GraphQL mutations and queries.
- **Field definitions**: Used to specify exactly which fields to retrieve in responses.
- **Enums**: Enumerated values accepted by the GPP schema (e.g., `Existence`, `AtomStage`).
- **Query/mutation builders**: DSL-style functions that construct strongly-typed operations.

These are essential when working with manager methods like ``create()``, ``update_by_id()``, and ``get_all()``, and enable full control over the structure of GraphQL operations without writing raw queries.

.. note::

   These modules are **auto-generated** and should not be modified manually. Instead, import them to build GraphQL inputs or access specific fields when constructing a query or mutation.

What's Included
---------------

The following submodules contain the core building blocks for working with GPP GraphQL operations.

Input Types
^^^^^^^^^^^

Use these when building input arguments for ``create()``, ``update_by_id()``, ``update_all()``, and other manager methods.

- :doc:`Input Types <input_types>`

Fields
^^^^^^

Use these to specify which fields to request in GraphQL queries or mutations.

- :doc:`Field Definitions <custom_fields>`

Queries
^^^^^^^

Use these builders to construct query operations.

- :doc:`Query Builders <custom_queries>`

Mutations
^^^^^^^^^

Use these builders to construct mutation operations.

- :doc:`Mutation Builders <custom_mutations>`

Enums
^^^^^

Use these for enum-constrained values when defining inputs.

- :doc:`Enum Types <enums>`

Module Reference
----------------

.. toctree::
   :maxdepth: 1

   input_types
   enums
   custom_fields
   custom_queries
   custom_mutations
