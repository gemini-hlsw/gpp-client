Observation
===========

The ``client.observation`` domain reads and changes observations. Most of its
methods take an observation ID (``o-...``) or a reference such as
``G-2026A-0001-Q-0001``.

Get an observation by reference
-------------------------------

Pass the reference to ``get_by_reference``:

.. code-block:: python

   result = await client.observation.get_by_reference(
       "G-2026A-0001-Q-0001"
   )
   observation = result.observation
   if observation is not None:
       print(
           observation.id,
           observation.title,
           observation.instrument,
       )
   # o-1a2 NGC 1068 Instrument.GMOS_NORTH

Update an observation
---------------------

To change an observation, pass an ``ObservationPropertiesInput`` as
``properties`` to ``update_by_id``. The client sends only the fields you set,
and the result lists the observations that GPP updated.

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

This example sets a new subtitle:

.. code-block:: python

   from gpp_client.generated.input_types import (
       ObservationPropertiesInput,
   )

   properties = ObservationPropertiesInput(
       subtitle="Second visit",
   )
   result = await client.observation.update_by_id(
       "o-1a2", properties=properties
   )
   updated = result.update_observations.observations
   for observation in updated:
       print(observation.id, observation.subtitle)
   # o-1a2 Second visit

API reference
-------------

.. autoclass:: gpp_client.domains.observation.ObservationDomain
   :members:
   :undoc-members:
