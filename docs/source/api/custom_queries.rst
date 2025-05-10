GraphQL Query Builders
======================

The ``gpp_client.api.custom_queries`` module defines statically typed query builders corresponding to GraphQL `Query` operations available in the GPP schema.

Each function or class in this module allows you to construct a well-formed GraphQL query by supplying the required arguments and selecting specific fields to return. These builders ensure correctness, help avoid typos, and provide autocomplete support when working in an IDE.

Query builders are typically used with ``.fields(...)`` to define the selection set:

.. code-block:: python

   from gpp_client.api.custom_queries import Query
   from gpp_client.api.custom_fields import ProgramFields

   query = Query.program(program_id="p-test").fields(
       ProgramFields.id,
       ProgramFields.name,
   )

These builders are passed directly to ``client.query(...)``:

.. code-block:: python

   result = await client.query(query, operation_name="program")

API Reference
-------------

.. automodule:: gpp_client.api.custom_queries
   :members:
   :undoc-members: