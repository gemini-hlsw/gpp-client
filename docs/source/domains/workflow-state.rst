Workflow state
==============

The ``client.workflow_state`` domain reads and changes an observation's
workflow. You can read the workflow by observation ID or reference, and change
the workflow by observation ID.

A workflow carries two states. The calculation state says whether GPP has
finished its background work on the observation. The workflow state is where
the observation stands, with the states it can move to next.

Read both states
----------------

This example reads both states, and the states the observation can move to:

.. code-block:: python

   result = await client.workflow_state.get_by_id(
       "o-1a2"
   )
   observation = result.observation
   if observation is not None:
       workflow = observation.workflow
       if workflow is not None:
           print(workflow.state)
           print(workflow.value.state)
           print(workflow.value.valid_transitions)

It prints the calculation state, the workflow state, and the states the
observation can move to, something like:

.. code-block:: text

   CalculationState.READY
   ObservationWorkflowState.DEFINED
   [<ObservationWorkflowState.READY: 'READY'>]

Change the workflow state
-------------------------

Before it sends a change, ``update_by_id`` checks the observation:

- If there's no such observation, it raises ``GPPValidationError``.
- If GPP returns no workflow, it raises ``GPPClientError``.
- If the calculation isn't ready, it raises ``GPPRetryableError``.
- If the observation is already in that state, it returns the current
  workflow and sends nothing.
- If the observation can't move to the new state, it raises
  ``GPPValidationError``.

.. warning::

   This call changes data in GPP. Try it on development first, as described
   in :ref:`try-on-development`.

This example moves an observation to ``READY`` and handles the two errors you
can act on:

.. code-block:: python

   from gpp_client.exceptions import (
       GPPRetryableError,
       GPPValidationError,
   )
   from gpp_client.generated.enums import (
       ObservationWorkflowState,
   )

   ready = ObservationWorkflowState.READY
   try:
       updated = await client.workflow_state.update_by_id(
           "o-1a2", workflow_state=ready
       )
       print(updated.state)
   except GPPRetryableError:
       print("Still calculating. Try again shortly.")
   except GPPValidationError as error:
       print("Not allowed:", error)
   # ObservationWorkflowState.READY

On the result of ``update_by_id``, ``.state`` is the workflow state. On the
result of ``get_by_id``, ``workflow.state`` is the calculation state, and the
workflow state is ``workflow.value.state``.

Retry while GPP calculates
--------------------------

The ``update_by_id_with_retry`` method does the same, but waits and tries
again while the calculation isn't ready. It retries only that case, up to
``max_attempts`` times, with ``retry_delay`` seconds between tries. Other
errors raise at once, and if the method runs out of attempts, it raises
``GPPClientError``.

API reference
-------------

.. autoclass:: gpp_client.domains.workflow_state.WorkflowStateDomain
   :members:
   :undoc-members:
