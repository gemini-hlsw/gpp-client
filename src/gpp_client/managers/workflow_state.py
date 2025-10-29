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
from ..api.enums import ObservationWorkflowState, CalculationState
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
        Get the workflow state and calculation state of an observation by its ID or
        reference.

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
        Update the workflow state of an observation by its ID, or return the current
        workflow if already set.

        This function will:
            - Fetch the current observation and its workflow.
            - If the calculation state is not ``READY``, raise an error to retry later.
            - If the desired state is already set, return the workflow as-is.
            - Otherwise, validate the requested workflow state against
              ``validTransitions``.
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

        Raises
        ------
        RuntimeError
            If the observation calculation is not in the ``READY`` state. Retry later.
        ValueError
            If the requested workflow state transition is not allowed.
        """
        result = await self.get_by_id(observation_id=observation_id)
        workflow = result["workflow"]

        # If calculation is not 'READY', raise an error to retry later.
        self._check_ready(workflow)
        # If the desired state is already set, return as-is.
        if self._check_already_set(workflow, workflow_state):
            # Return the same shape as other return paths.
            return workflow["value"]
        # Validate the requested workflow state against 'validTransitions'.
        self._check_valid_transition(workflow, workflow_state)

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
    def _check_ready(workflow: dict[str, Any]) -> None:
        """
        Raise an error if the observation calculation is not in the ``READY`` state.

        Parameters
        ----------
        workflow : dict[str, Any]
            The workflow data structure returned by ``get_by_id()``.

        Raises
        ------
        RuntimeError
            If the calculation state is not ``READY``.
        """
        if workflow["state"] != CalculationState.READY.value:
            raise RuntimeError(
                "Observation calculation is not READY (current state: "
                f"{workflow['state']}). Please retry after background processing "
                "is complete."
            )

    @staticmethod
    def _check_already_set(
        workflow: dict[str, Any],
        workflow_state: ObservationWorkflowState,
    ) -> bool:
        """
        Check if the workflow is already set to the desired state.

        Parameters
        ----------
        workflow : dict[str, Any]
            The workflow data structure returned by ``get_by_id()``.
        workflow_state : ObservationWorkflowState
            The desired workflow state.

        Returns
        -------
        bool
            ``True`` if the current workflow state matches the desired state,
            otherwise ``False``.
        """
        return workflow["value"]["state"] == workflow_state.value

    @staticmethod
    def _check_valid_transition(
        workflow: dict[str, Any],
        workflow_state: ObservationWorkflowState,
    ) -> None:
        """
        Validate that the desired workflow state is allowed as a transition.

        Parameters
        ----------
        workflow : dict[str, Any]
            The workflow data structure returned by ``get_by_id()``.
        workflow_state : ObservationWorkflowState
            The desired workflow state to transition to.

        Raises
        ------
        ValueError
            If the requested transition is not allowed based on
            ``validTransitions``.
        """
        valid_transitions = workflow["value"].get("validTransitions", [])
        if workflow_state.value not in valid_transitions:
            valid_str = ", ".join(valid_transitions) or "None"
            raise ValueError(
                f"Cannot transition to '{workflow_state.value}'. "
                f"Valid transitions are: {valid_str}."
            )

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
