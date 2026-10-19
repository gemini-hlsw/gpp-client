GraphQL API
===========

These pages describe the code that the build generates from GPP's GraphQL
schema. Most users only need the domains, but these pages help you build an input, read a result
field, or write a custom query.

.. list-table::
   :header-rows: 1

   * - Page
     - Use it to
   * - :doc:`input-types`
     - Build the input a method takes.
   * - :doc:`enums`
     - Pass or compare enum values.
   * - :doc:`result-models`
     - See the fields a method returns.
   * - :doc:`field-builders`, :doc:`custom-queries`, :doc:`custom-mutations`
     - Write a custom query.
   * - :doc:`client`
     - Call a generated operation directly.
   * - :doc:`exceptions`
     - Catch errors GPP returns for a GraphQL call.

.. toctree::
   :hidden:

   input-types
   enums
   result-models
   client
   field-builders
   custom-queries
   custom-mutations
   exceptions

Internal modules
----------------

The pages above link to types from these internal modules. You shouldn't need
them, but they're here so that every type link leads somewhere:

- :doc:`base-model` - the shared Pydantic base model and the ``UNSET`` marker.
- :doc:`operation-builder` - the base classes for the fields and arguments
  of a custom operation.
- :doc:`transport-client` - the client that sends each request to GPP.
- :doc:`typed-field-helpers` - the field classes that the field builders
  return.
