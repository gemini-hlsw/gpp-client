GraphQL Mutation Builders
=========================

The ``gpp_client.api.custom_mutations`` module defines typed builders for all GraphQL mutation operations in the GPP schema.

These builders construct mutation payloads using validated input types and ensure correct GraphQL syntax. Each mutation accepts an input object (typically a ``Create*Input`` or ``Update*Input``) and supports ``.fields(...)`` to specify which fields should be returned from the mutation result.

Usage Example
-------------

.. code-block:: python

   from gpp_client.api.custom_mutations import Mutation
   from gpp_client.api.custom_fields import CreateTargetResultFields
   from gpp_client.api.input_types import CreateTargetInput, TargetPropertiesInput

   input_data = CreateTargetInput(
       program_id="p-test",
       set=TargetPropertiesInput(name="Target A", ...)
   )

   mutation = Mutation.create_target(input=input_data).fields(
       CreateTargetResultFields.target().fields(
           # Specify fields to return.
       )
   )

   result = await client.mutation(mutation, operation_name="createTarget")

API Reference
-------------

.. automodule:: gpp_client.api.custom_mutations
   :members:
   :undoc-members: