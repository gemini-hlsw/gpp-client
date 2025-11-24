__all__ = ["WorkflowStateManager"]

import asyncio
import logging
from typing import Any, Optional

from gpp_client.api.custom_fields import (
    CalculatedObservationWorkflowFields,
    ObservationFields,
    ObservationReferenceFields,
    ObservationValidationFields,
    ObservationWorkflowFields,
)
from gpp_client.api.custom_mutations import Mutation
from gpp_client.api.custom_queries import Query
from gpp_client.api.enums import CalculationState, ObservationWorkflowState
from gpp_client.api.input_types import SetObservationWorkflowStateInput
from gpp_client.exceptions import GPPClientError, GPPRetryableError, GPPValidationError
from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)


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

        Raises
        ------
        GPPValidationError
            If neither or both of ``observation_id`` and ``observation_reference``
            are provided.
        GPPClientError
            If neither or both of ``observation_id`` and ``observation_reference``
            are provided, or if the observation cannot be found.
        """
        logger.debug(
            "Fetching workflow state for observation ID %s or reference %s",
            observation_id,
            observation_reference,
        )
        self.validate_single_identifier(
            observation_id=observation_id,
            observation_reference=observation_reference,
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

        return self.get_result(result, operation_name)

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
        GPPClientError
            If there are general client-side errors.
        GPPValidationError
            If the requested workflow state transition is invalid.
        GPPRetryableError
            If the observation calculation is not ``READY``.
        """
        logger.debug(
            "Updating workflow state for observation ID %s to %s",
            observation_id,
            workflow_state.value,
        )
        result = await self.get_by_id(observation_id=observation_id)
        workflow = result["workflow"]

        # If calculation is not 'READY', raise an error to retry later.
        try:
            self._check_ready(workflow)
        except RuntimeError as exc:
            self.raise_error(GPPRetryableError, exc)

        # If the desired state is already set, return as-is.
        if self._check_already_set(workflow, workflow_state):
            # Return the same shape as other return paths.
            logger.debug(
                "Workflow state for observation ID %s is already %s; no update needed.",
                observation_id,
                workflow_state.value,
            )
            return workflow["value"]
        # Validate the requested workflow state against 'validTransitions'.
        try:
            self._check_valid_transition(workflow, workflow_state)
        except ValueError as exc:
            self.raise_error(GPPValidationError, exc)

        input_data = SetObservationWorkflowStateInput(
            observation_id=observation_id,
            state=workflow_state,
        )

        fields = Mutation.set_observation_workflow_state(input=input_data).fields(
            *self._fields()
        )

        operation_name = "setObservationWorkflowState"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def update_by_id_with_retry(
        self,
        *,
        workflow_state: ObservationWorkflowState,
        observation_id: str,
        max_attempts: int = 10,
        initial_delay: float = 0.0,
        retry_delay: float = 1.0,
    ) -> dict[str, Any]:
        """
        Update the workflow state of an observation by its ID, retrying if the
        observation is not ready.

        This function wraps ``update_by_id`` with retry logic to handle cases where
        the observation calculation is not yet in the ``READY`` state.

        Parameters
        ----------
        workflow_state : ObservationWorkflowState
            The desired workflow state to transition to.
        observation_id : str
            The observation ID.
        max_attempts : int, default=10
            Maximum number of retry attempts.
        initial_delay : float, default=0.0
            Initial delay in seconds before first attempt.
        retry_delay : float, default=1.0
            Delay in seconds between retry attempts.

        Returns
        -------
        dict[str, Any]
            The returned workflow state for the observation.

        Raises
        ------
        GPPClientError
            If the maximum number of retry attempts is exceeded without success.
        GPPValidationError
            If the requested workflow state transition is invalid.
        """
        logger.debug(
            "Updating workflow state for observation ID %s to %s with up to %d retries",
            observation_id,
            workflow_state.value,
            max_attempts,
        )
        logger.debug("Initial delay before first attempt: %.1f seconds", initial_delay)
        await asyncio.sleep(initial_delay)

        for attempt in range(1, max_attempts + 1):
            try:
                logger.debug(
                    "Attempt %d/%d: Updating workflow state for observation ID %s to %s",
                    attempt,
                    max_attempts,
                    observation_id,
                    workflow_state.value,
                )
                result = await self.update_by_id(
                    observation_id=observation_id,
                    workflow_state=workflow_state,
                )
                return result
            except GPPRetryableError:
                # This is the only retryable case: calculation state not READY.
                await asyncio.sleep(retry_delay)
            except (GPPValidationError, GPPClientError) as exc:
                self.raise_error(type(exc), exc)

        exc = GPPClientError("Failed to set workflow state after multiple retries.")
        self.raise_error(type(exc), exc)

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
