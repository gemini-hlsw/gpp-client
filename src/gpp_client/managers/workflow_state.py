__all__ = ["WorkflowStateManager"]

from typing import Any, Optional

from ..api.custom_fields import (
    CalculatedObservationWorkflowFields,
    ObservationFields,
    ObservationReferenceFields,
    ObservationValidationFields,
    ObservationWorkflowFields,
)
from ..api.custom_mutations import Mutation
from ..api.custom_queries import Query
from ..api.enums import ObservationWorkflowState
from ..api.input_types import SetObservationWorkflowStateInput
from .base import BaseManager
from .utils import validate_single_identifier


class WorkflowStateManager(BaseManager):
    async def get_by_id(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Get the workflow state of an observation by its ID or reference.

        Parameters
        ----------
        observation_id : Optional[str], optional
            The observation ID, by default ``None``.
        observation_reference : Optional[str], optional
            The observation reference, by default ``None``.

        Returns
        -------
        dict[str, Any]
            The returned workflow state for the observation.
        """
        validate_single_identifier(
            observation_id=observation_id, observation_reference=observation_reference
        )

        fields = Query.observation(
            observation_id=observation_id, observation_reference=observation_reference
        ).fields(
            ObservationFields.id,
            ObservationFields.reference().fields(
                ObservationReferenceFields.label,
            ),
            ObservationFields.workflow().fields(
                CalculatedObservationWorkflowFields.state,
                CalculatedObservationWorkflowFields.value().fields(*self._fields()),
            ),
        )

        operation_name = "observation"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_by_id(
        self,
        *,
        workflow_state: ObservationWorkflowState,
        observation_id: str,
    ) -> dict[str, Any]:
        """
        Update the workflow state of an observation by its ID or reference.

        This function will:
            - Fetch the current observation and its workflow.
            - Check if the calculation state is ``READY``.
            - Validate the requested workflow state against ``validTransitions``.
            - If valid, submit the mutation to update the workflow state.

        Parameters
        ----------
        workflow_state : ObservationWorkflowState
            The desired workflow state to transition to.
        observation_id : str
            The observation ID.

        Returns
        -------
        dict[str, Any]
            The returned workflow state for the observation.
        """
        result = await self.get_by_id(observation_id=observation_id)
        workflow = result["workflow"]

        if not self._can_transition_to(workflow_state, workflow):
            valid_transitions = ", ".join(workflow["value"].get("validTransitions", []))

            raise ValueError(
                f"Cannot transition to '{workflow_state.value}': "
                f"calculation state = '{workflow['state']}', "
                f"valid transitions = {valid_transitions}"
            )

        input_data = SetObservationWorkflowStateInput(
            observation_id=observation_id,
            state=workflow_state,
        )

        fields = Mutation.set_observation_workflow_state(input=input_data).fields(
            *self._fields()
        )

        operation_name = "setObservationWorkflowState"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    @staticmethod
    def _can_transition_to(
        desired_state: ObservationWorkflowState,
        workflow: dict[str, Any],
    ) -> bool:
        """
        Check if the observation workflow can transition to the desired state.

        Parameters
        ----------
        desired_state : ObservationWorkflowState
            The target state you want to transition to.

        workflow : dict[str, Any]
            The current workflow data from the observation, including 'state',
            'value', and its nested 'validTransitions'.

        Returns
        -------
        bool
            ``True`` if the transition is allowed and calculation state is ``READY``.
        """
        if workflow["state"] != "READY":
            return False
        return desired_state in workflow["value"].get("validTransitions", [])

    @staticmethod
    def _fields() -> tuple:
        """
        Return the GraphQL fields to retrieve for observation workflow.

        Returns
        -------
        tuple
            Field selections for observation workflow queries.
        """
        return (
            ObservationWorkflowFields.state,
            ObservationWorkflowFields.valid_transitions,
            ObservationWorkflowFields.validation_errors().fields(
                ObservationValidationFields.code,
                ObservationValidationFields.messages,
            ),
        )
