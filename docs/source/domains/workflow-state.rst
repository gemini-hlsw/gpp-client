Workflow State
==============

The workflow state domain provides access to observation workflow state queries
and updates.

Use :attr:`~gpp_client.GPPClient.workflow_state` to inspect workflow state and
transition observations through valid workflow stages.

Quick Example
-------------

.. code-block:: python

   from gpp_client.generated import ObservationWorkflowState

   async with GPPClient() as client:
      result = await client.workflow_state.update_by_id(
         observation_id="o-123",
         workflow_state=ObservationWorkflowState.READY,
      )


Retrieving Workflow State
-------------------------

Get workflow state by observation ID:

.. code-block:: python

   result = await client.workflow_state.get_by_id("o-123")

Get workflow state by observation reference:

.. code-block:: python

   result = await client.workflow_state.get_by_reference("GN-2026A-Q-1-1")


Updating Workflow State
-----------------------

Update workflow state by observation ID:

.. code-block:: python

   result = await client.workflow_state.update_by_id(
      observation_id="o-123",
      workflow_state=workflow_state,
   )

The domain validates that:

- The observation calculation state is ready
- The requested transition is valid
- The workflow state is not already set


Retrying Workflow Updates
-------------------------

Use ``update_by_id_with_retry`` to retry while background calculation is still
in progress:

.. code-block:: python

   result = await client.workflow_state.update_by_id_with_retry(
      observation_id="o-123",
      workflow_state=workflow_state,
      max_attempts=10,
      retry_delay=1.0,
   )

This is useful when workflow updates depend on calculation state becoming ready.


Error Handling
--------------

Workflow state updates may raise:

- ``GPPRetryableError`` when calculation state is not ready
- ``GPPValidationError`` for invalid workflow transitions
- ``GPPClientError`` for other client-side failures


Notes
-----

All workflow state operations use GraphQL.

The retry helper only retries the not-ready case. Validation and other client
errors fail immediately.


API Reference
-------------

.. autoclass:: gpp_client.domains.workflow_state.WorkflowStateDomain
   :members:
   :exclude-members: __init__