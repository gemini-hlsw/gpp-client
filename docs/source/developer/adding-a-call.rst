Add or change a call
====================

Most code changes add or change one call on a domain, such as
``client.program.get_by_id``. Each domain method wraps one generated GraphQL
method. The steps below use the program domain, so swap in your own domain
where yours differs.

1. Write the operation in the ``graphql/operations/domains/program/`` folder.
   Queries go in ``queries.graphql``, and mutations go in
   ``mutations.graphql``. For example, this query gets one program:

   .. code-block:: graphql

      query getProgramById($programId: ProgramId!, $includeDeleted: Boolean! = false) {
        program(programId: $programId) {
          ...ProgramDetail
          ...ProgramGroupElements
        }
      }

   Write the operation once for every environment, because the build trims it
   for each one.

2. Rebuild the client:

   .. code-block:: bash

      uv run --group codegen python -m scripts.build_client

   The build adds ``get_program_by_id`` to ``client.graphql`` and a result
   model, ``GetProgramById``, under ``src/gpp_client/generated/``. Never edit
   those generated files. If the build fails, see :doc:`updating-the-schema`.

3. Add the domain method in ``src/gpp_client/domains/program.py``. The method
   calls the generated method and returns its result:

   .. docs-guard: skip - a method of ProgramDomain, not a standalone example

   .. code-block:: python

      async def get_by_id(
          self,
          program_id: str,
          *,
          include_deleted: bool = False,
      ) -> GetProgramById:
          """
          Get a program by ID.

          Parameters
          ----------
          program_id : str
              The program ID.
          include_deleted : bool, default=False
              Whether deleted related records should be included.

          Returns
          -------
          GetProgramById
              The generated GraphQL response model.
          """
          return await self._graphql.get_program_by_id(
              program_id=program_id,
              include_deleted=include_deleted,
          )

   The docstring follows the numpydoc style. A commit hook checks it, and the
   reference page is built from it.

4. Add a test in ``tests/gpp_client/domains/test_program.py``. Mock the
   generated method and check that the domain passes its arguments through.
   For a plain pass-through, add a row to the parametrized dispatch test in
   that file instead.

5. Run the domain tests:

   .. code-block:: bash

      uv run pytest tests/gpp_client/domains

6. Optional: for a call that users will reach for, add an example to
   ``docs/source/domains/program.rst``, as described in :doc:`documentation`.

7. Commit the operation, the generated code, the domain method, and its test
   together.
