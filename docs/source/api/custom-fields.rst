Field Selectors
===============

The ``gpp_client.api.custom_fields`` module contains statically defined field selectors used to build GraphQL queries and mutations.

These fields mirror the GraphQL schema's object types and can be used to explicitly select which fields to return when performing operations via the GPP Client. This allows for fine-grained control over response data and avoids overfetching.

For example, to fetch only a program's ID and name:

.. code-block:: python

   from gpp_client.api.custom_fields import ProgramFields

   fields = ProgramFields.id, ProgramFields.name

These field selectors are typically used in conjunction with the ``fields()`` method on query or mutation builders:

.. code-block:: python

   fields = Query.program(program_id="p-test").fields(
       ProgramFields.id,
       ProgramFields.name,
   )

API Reference
-------------

.. automodule:: gpp_client.api.custom_fields
   :members:
   :undoc-members:
