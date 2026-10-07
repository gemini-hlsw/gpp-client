Program
=======

The ``client.program`` domain reads and changes programs. You can look up a
program by its ID, its program reference or its proposal reference. The
examples below use the ID.

Get a program by ID
-------------------

Pass the ID to ``get_by_id``. The result's ``program`` is ``None`` if no
program has that ID:

.. code-block:: python

   result = await client.program.get_by_id("p-10a")
   if result.program is not None:
       print(result.program.name)
   # Galaxy survey

Find programs with a filter
---------------------------

To find programs that match a filter, pass a ``WhereProgram`` input as the
``where`` argument. The result's ``has_more`` tells you whether more programs
match than ``limit`` returned:

.. code-block:: python

   from gpp_client.generated.input_types import (
       WhereOptionString,
       WhereProgram,
   )

   name = WhereOptionString(
       like="%survey%",
       match_case=False,
   )
   result = await client.program.get_all(
       where=WhereProgram(name=name),
       limit=10,
   )
   for program in result.programs.matches:
       print(program.id, program.name)
   # p-10a Galaxy survey
   print(result.programs.has_more)
   # False

Get every program
-----------------

To get every program, page through the results. Pass the last ID from one page
as ``offset`` to get the next. Each new page starts with that same program, so
the loop skips it:

.. code-block:: python

   offset = None
   while True:
       result = await client.program.get_all(
           offset=offset,
           limit=100,
       )
       matches = result.programs.matches
       if offset is not None and matches:
           if matches[0].id == offset:
               matches = matches[1:]
       for program in matches:
           print(program.id, program.name)
       if not result.programs.has_more or not matches:
           break
       offset = matches[-1].id

API reference
-------------

.. autoclass:: gpp_client.domains.program.ProgramDomain
   :members:
   :undoc-members:
