GOATS
=====

The ``client.goats`` domain runs the queries built for GOATS. They return:

- accepted programs
- the observations in an accepted program
- a program's approved configuration requests
- the configuration options for an instrument

This example lists the observations in the first three accepted programs:

.. code-block:: python

   goats = client.goats
   accepted = await goats.get_programs()
   for program in accepted.programs.matches[:3]:
       result = await goats.get_observations_by_program_id(
           program_id=program.id
       )
       for obs in result.observations.matches:
           print(program.id, obs.id, obs.title)
   # p-10a o-1a2 NGC 1068

Each program takes one call, and the calls run one after another. So slice
the list to the programs you need.

API reference
-------------

.. autoclass:: gpp_client.domains.goats.GOATSDomain
   :members:
   :undoc-members:
