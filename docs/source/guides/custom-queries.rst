Write a custom query
====================

When no domain method fits, you can build the query yourself and select
exactly the fields you need.

Build and send a query
----------------------

Start from a root field on ``Query``, then select the fields you want with
``.fields(...)``. Each type has a ``<Type>Fields`` class in
``gpp_client.generated.custom_fields`` that lists its fields:

.. code-block:: python

   from gpp_client.generated.custom_fields import (
       ProgramFields,
   )
   from gpp_client.generated.custom_queries import (
       Query,
   )

   data = await client.graphql.query(
       Query.program(program_id="p-10a").fields(
           ProgramFields.id,
           ProgramFields.name,
           ProgramFields.proposal_status,
       ),
       operation_name="programName",
   )
   program = data["program"]
   if program is None:
       print("No program with that ID.")
   else:
       print(
           program["id"],
           program["name"],
           program["proposalStatus"],
       )
   # p-10a Galaxy survey ACCEPTED

The ``client.graphql.query`` method returns GPP's ``data`` as a plain
dictionary. Its keys are the GraphQL names, in camelCase, so you read
``proposalStatus``, not ``proposal_status``. If a lookup finds nothing, its
key holds ``None``.

The ``operation_name`` argument is required, because it names the operation
that the client sends to GPP. To ask for several root fields at once, pass
each one to ``query`` as its own argument.

Select nested fields
--------------------

Fields that hold objects are methods, such as ``ProgramFields.pi()``. Call the
method, then select its fields with ``.fields(...)``:

.. code-block:: python

   from gpp_client.generated.custom_fields import (
       ProgramFields,
       ProgramUserFields,
   )
   from gpp_client.generated.custom_queries import (
       Query,
   )

   pi = ProgramFields.pi().fields(
       ProgramUserFields.display_name,
   )
   data = await client.graphql.query(
       Query.program(program_id="p-10a").fields(
           ProgramFields.name,
           pi,
       ),
       operation_name="programPi",
   )
   program = data["program"]
   if program is not None and program["pi"]:
       print(program["pi"]["displayName"])
   # Ada Lovelace

Send a mutation
---------------

Mutations work the same way. Start from a root field on ``Mutation``, and send
it with ``client.graphql.mutation``.

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

This example creates a program and prints its new ID:

.. code-block:: python

   from gpp_client.generated.custom_fields import (
       CreateProgramResultFields,
       ProgramFields,
   )
   from gpp_client.generated.custom_mutations import (
       Mutation,
   )
   from gpp_client.generated.input_types import (
       CreateProgramInput,
       ProgramPropertiesInput,
   )

   properties = ProgramPropertiesInput(
       name="My program",
   )
   create = Mutation.create_program(
       input=CreateProgramInput(set_=properties),
   )
   program = CreateProgramResultFields.program()
   data = await client.graphql.mutation(
       create.fields(program.fields(ProgramFields.id)),
       operation_name="createProgram",
   )
   print(data["createProgram"]["program"]["id"])
   # p-10c

Send a GraphQL document as text
-------------------------------

If you already have the GraphQL text, send it with the ``execute`` method.
Then unpack the response with the ``get_data`` method:

.. code-block:: python

   document = """
   query programName($id: ProgramId!) {
     program(programId: $id) { name }
   }
   """
   response = await client.graphql.execute(
       document,
       operation_name="programName",
       variables={"id": "p-10a"},
   )
   data = client.graphql.get_data(response)
   print(data["program"])
   # {'name': 'Galaxy survey'}

Check against the environment
-----------------------------

The client checks every custom query, mutation and document against the
selected environment before it sends it. If the query uses something that
the selected environment lacks but the other environment has, the client
raises ``GPPEnvironmentError`` and sends nothing. For details, see :ref:`environment-errors`.

Reference
---------

- :doc:`../graphql-api/custom-queries` - the root fields on ``Query``.
- :doc:`../graphql-api/custom-mutations` - the root fields on ``Mutation``.
- :doc:`../graphql-api/field-builders` - the ``Fields`` classes.
