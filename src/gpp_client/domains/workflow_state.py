"""
Module for managing observation workflow states in the GPP client.
"""

__all__ = ["WorkflowStateDomain"]

import asyncio
import logging

from gpp_client.domains.base import BaseDomain
from gpp_client.exceptions import (
    GPPClientError,
    GPPRetryableError,
    GPPValidationError,
    GPPWorkflowTransitionError,
    WorkflowReason,
)
from gpp_client.generated.enums import CalculationState, ObservationWorkflowState
from gpp_client.generated.get_observation_workflow_state_by_id import (
    GetObservationWorkflowStateById,
    GetObservationWorkflowStateByIdObservation,
    GetObservationWorkflowStateByIdObservationWorkflow,
)
from gpp_client.generated.get_observation_workflow_state_by_reference import (
    GetObservationWorkflowStateByReference,
)
from gpp_client.generated.set_observation_workflow_state import (
    SetObservationWorkflowStateSetObservationWorkflowState,
)

logger = logging.getLogger(__name__)


class WorkflowStateDomain(BaseDomain):
    """
    Domain for managing observation workflow states.
    """

    async def get_by_id(
        self,
        observation_id: str,
    ) -> GetObservationWorkflowStateById:
        """
        Get workflow state details for an observation by ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.

        Returns
        -------
        GetObservationWorkflowStateById
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation_workflow_state_by_id(
            observation_id=observation_id
        )

    async def get_by_reference(
        self,
        observation_reference: str,
    ) -> GetObservationWorkflowStateByReference:
        """
        Get workflow state details for an observation by reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.

        Returns
        -------
        GetObservationWorkflowStateByReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation_workflow_state_by_reference(
            observation_reference=observation_reference
        )

    async def update_by_id(
        self,
        observation_id: str,
        *,
        workflow_state: ObservationWorkflowState,
    ) -> SetObservationWorkflowStateSetObservationWorkflowState:
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
        observation_id : str
            The observation ID.
        workflow_state : ObservationWorkflowState
            The desired workflow state to transition to.

        Returns
        -------
        SetObservationWorkflowStateSetObservationWorkflowState
            The workflow details for the observation after the operation.

        Raises
        ------
        GPPClientError
            If there are general client-side errors.
        GPPWorkflowTransitionError
            If GPP does not allow the requested state; it carries GPP's reasons.
        GPPRetryableError
            If the observation calculation is not ``READY``.
        """
        logger.debug(
            "Updating workflow state for observation ID %s to %s",
            observation_id,
            workflow_state.value,
        )
        result = await self.get_by_id(observation_id=observation_id)
        workflow = result.observation.workflow

        # If calculation is not 'READY', raise an error to retry later.
        try:
            _check_ready(workflow)
        except RuntimeError as exc:
            self.raise_error(GPPRetryableError, exc)

        # If the desired state is already set, return the current workflow
        # rebuilt as the mutation response model.
        if _check_already_set(workflow, workflow_state):
            logger.debug(
                "Workflow state for observation ID %s is already %s; no update needed.",
                observation_id,
                workflow_state.value,
            )
            return (
                SetObservationWorkflowStateSetObservationWorkflowState.model_validate(
                    workflow.value.model_dump(by_alias=True)
                )
            )
        # Validate the requested workflow state against 'validTransitions'. The
        # error goes out as raised, since raise_error would drop its reasons.
        try:
            _check_valid_transition(workflow, workflow_state)
        except GPPWorkflowTransitionError as exc:
            logger.error("%s: %s", type(self).__name__, exc)
            raise

        mutation_result = await self._graphql.set_observation_workflow_state(
            observation_id=observation_id,
            state=workflow_state,
        )
        payload = mutation_result.set_observation_workflow_state
        if payload is None:
            raise GPPClientError(
                "GPP returned no payload for setObservationWorkflowState."
            )
        return payload

    async def update_by_id_with_retry(
        self,
        observation_id: str,
        *,
        workflow_state: ObservationWorkflowState,
        max_attempts: int = 10,
        initial_delay: float = 0.0,
        retry_delay: float = 1.0,
    ) -> SetObservationWorkflowStateSetObservationWorkflowState:
        """
        Update the workflow state of an observation by its ID, retrying if the
        observation is not ready.

        This function wraps ``update_by_id`` with retry logic to handle cases where
        the observation calculation is not yet in the ``READY`` state.

        Parameters
        ----------
        observation_id : str
            The observation ID.
        workflow_state : ObservationWorkflowState
            The desired workflow state to transition to.
        max_attempts : int, default=10
            Maximum number of retry attempts.
        initial_delay : float, default=0.0
            Initial delay in seconds before first attempt.
        retry_delay : float, default=1.0
            Delay in seconds between retry attempts.

        Returns
        -------
        SetObservationWorkflowStateSetObservationWorkflowState
            The workflow details for the observation after the operation.

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
                if attempt < max_attempts:
                    await asyncio.sleep(retry_delay)
            except (GPPValidationError, GPPClientError):
                # update_by_id already logged it.
                raise

        exc = GPPClientError("Failed to set workflow state after multiple retries.")
        self.raise_error(type(exc), exc)

    async def get_by_id_when_ready(
        self,
        observation_id: str,
        *,
        max_attempts: int = 10,
        initial_delay: float = 0.0,
        retry_delay: float = 1.0,
    ) -> GetObservationWorkflowStateByIdObservation:
        """
        Get an observation's workflow once GPP has finished calculating it.

        After an edit, GPP recalculates the observation in the background, and its
        workflow (state, valid transitions and validation errors) stays out of date
        until the calculation state is ``READY``.

        Parameters
        ----------
        observation_id : str
            The observation ID.
        max_attempts : int, default=10
            Maximum number of times to ask.
        initial_delay : float, default=0.0
            Delay in seconds before asking the first time.
        retry_delay : float, default=1.0
            Delay in seconds between asks.

        Returns
        -------
        GetObservationWorkflowStateByIdObservation
            The observation, with its workflow as calculated and the warnings its
            program dismissed, which do not keep it from ``READY``.

        Raises
        ------
        GPPClientError
            If GPP returns no such observation, or has not finished calculating it
            after every attempt.
        """
        await asyncio.sleep(initial_delay)
        for attempt in range(1, max_attempts + 1):
            result = await self.get_by_id(observation_id=observation_id)
            observation = result.observation
            if observation is None or observation.workflow is None:
                exc = GPPClientError(f"GPP returned no workflow for {observation_id}.")
                self.raise_error(type(exc), exc)
            if observation.workflow.state == CalculationState.READY:
                return observation
            if attempt < max_attempts:
                await asyncio.sleep(retry_delay)

        exc = GPPClientError("GPP did not finish calculating the observation in time.")
        self.raise_error(type(exc), exc)


def _check_ready(workflow: GetObservationWorkflowStateByIdObservationWorkflow) -> None:
    """
    Raise an error if the observation calculation is not in the ``READY`` state.

    Parameters
    ----------
    workflow : GetObservationWorkflowStateByIdObservationWorkflow
        The workflow Pydantic model returned by ``get_by_id().observation.workflow``.

    Raises
    ------
    RuntimeError
        If the calculation state is not ``READY``.
    """
    if workflow.state != CalculationState.READY:
        raise RuntimeError(
            "Observation calculation is not READY (current state: "
            f"{workflow.state.value}). Please retry after background processing "
            "is complete."
        )


def _check_already_set(
    workflow: GetObservationWorkflowStateByIdObservationWorkflow,
    workflow_state: ObservationWorkflowState,
) -> bool:
    """
    Check if the workflow is already set to the desired state.

    Parameters
    ----------
    workflow : GetObservationWorkflowStateByIdObservationWorkflow
        The workflow Pydantic model returned by ``get_by_id().observation.workflow``.
    workflow_state : ObservationWorkflowState
        The desired workflow state.

    Returns
    -------
    bool
        ``True`` if the current workflow state matches the desired state,
        otherwise ``False``.
    """
    return workflow.value.state == workflow_state


def _check_valid_transition(
    workflow: GetObservationWorkflowStateByIdObservationWorkflow,
    workflow_state: ObservationWorkflowState,
) -> None:
    """
    Validate that the desired workflow state is allowed as a transition.

    Parameters
    ----------
    workflow : GetObservationWorkflowStateByIdObservationWorkflow
        The workflow Pydantic model returned by ``get_by_id().observation.workflow``.
    workflow_state : ObservationWorkflowState
        The desired workflow state to transition to.

    Raises
    ------
    GPPWorkflowTransitionError
        If the requested transition is not allowed based on
        ``validTransitions``. It carries GPP's validation messages, which say
        why (for example, that no science band is selected), errors first. Its
        message gives them too, or else the states GPP allows.
    """
    valid_transitions = workflow.value.valid_transitions or []
    if workflow_state in valid_transitions:
        return

    # A code GPP sends without messages is still a reason.
    reasons = [
        WorkflowReason(
            severity=error.severity.value,
            code=error.code.value,
            message=message,
        )
        for error in workflow.value.validation_errors or []
        for message in (error.messages or [error.code.value])
    ]
    # Errors are what keeps the state from changing, so they come first.
    reasons.sort(key=lambda reason: reason.severity != "ERROR")
    allowed = [t.value for t in valid_transitions]

    if reasons:
        text = " ".join(reason.message for reason in reasons)
        message = f"Cannot change to {workflow_state.value}: {text}"
    else:
        message = (
            f"Cannot change to {workflow_state.value}. "
            f"GPP allows: {', '.join(allowed) or 'none'}."
        )
    raise GPPWorkflowTransitionError(
        message,
        requested=workflow_state.value,
        allowed=allowed,
        reasons=reasons,
    )
