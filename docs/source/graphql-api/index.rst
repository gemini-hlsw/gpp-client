GraphQL API
===========

This section documents the auto-generated models and helpers used by the
GPP client.

These modules are generated from the GraphQL schema and provide:

- Typed inputs for mutations and queries
- Structured response models
- Utilities for building custom GraphQL operations

In most cases, you should prefer :class:`~gpp_client.GPPClient` and its
domains.

The generated modules are most useful when you need to:

- Construct complex input payloads
- Inspect exact response model fields
- Build custom queries or mutations

.. note::

   These modules are auto-generated and should not be modified manually.

Modules
-------

The following modules are the primary entry points for advanced usage.

.. toctree::
   :maxdepth: 1

   input-types
   enums
   result-models
   client
   field-builders
   custom-queries
   custom-mutations
   exceptions

Low-level Helpers
-----------------

These pages document lower-level generated helpers used internally by the
GraphQL client implementation.

.. toctree::
   :maxdepth: 1

   base-model
   operation-builder
   transport-client
   typed-field-helpers