Scheduler
=========

The ``client.scheduler`` domain fetches the program and observation data that
the Gemini scheduler needs.

Get scheduler programs
----------------------

To get scheduler programs, call ``get_programs``. You can limit the result to
a list of program IDs. The client fetches every page and returns the pages as
one result:

.. code-block:: python

   result = await client.scheduler.get_programs(
       programs_list=["p-10a", "p-10b"],
   )
   for program in result.programs.matches:
       print(program.id)
   # p-10a

Get visibility changes
----------------------

To get the observations and targets whose visibility inputs changed at or
after a time, call ``get_visibility_changes``. A time without a time zone
counts as UTC:

.. code-block:: python

   from datetime import UTC, datetime, timedelta

   since = datetime.now(UTC) - timedelta(hours=1)
   changes = await client.scheduler.get_visibility_changes(
       since
   )
   print(sorted(changes.observation_ids))
   # ['o-1a2']
   print(sorted(changes.target_ids))
   # ['t-3b4']
   print(changes.max_timestamp)
   # 2026-10-05 14:02:11+00:00

The result's ``observation_ids`` and ``target_ids`` are sets of IDs. Its
``max_timestamp`` is the time of the latest change, or ``None`` when GPP
reported no time.

The ``get_visibility_changes`` method can raise these errors:

- ``GPPEnvironmentError`` when the selected environment doesn't serve
  visibility changes.
- ``aiohttp.ClientResponseError`` for other HTTP errors.
- ``aiohttp.ClientError`` when it can't connect.

Only ``GPPEnvironmentError`` is a ``GPPError``. For more, see
:doc:`../guides/errors`.

API reference
-------------

.. autoclass:: gpp_client.domains.scheduler.SchedulerDomain
   :members:
   :undoc-members:
