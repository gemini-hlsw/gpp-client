"""
Tests for the workflow state domain.
"""

from unittest.mock import call

import pytest

from gpp_client.domains.workflow_state import (
    WorkflowStateDomain,
    _check_already_set,
    _check_ready,
    _check_valid_transition,
)
from gpp_client.exceptions import GPPClientError, GPPRetryableError, GPPValidationError
from gpp_client.generated.enums import CalculationState, ObservationWorkflowState


@pytest.fixture()
def workflow_state_domain(domain_kwargs) -> WorkflowStateDomain:
    """
    Return a workflow state domain instance.
    """
    return WorkflowStateDomain(**domain_kwargs)


@pytest.mark.asyncio
async def test_get_by_id_dispatches_correctly(
    workflow_state_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure get_by_id dispatches to GraphQL.
    """
    result_model = object()
    graphql.get_observation_workflow_state_by_id = mocker.AsyncMock(
        return_value=result_model
    )

    result = await workflow_state_domain.get_by_id(observation_id="o-1")

    assert result is result_model
    graphql.get_observation_workflow_state_by_id.assert_called_once_with(
        observation_id="o-1"
    )


@pytest.mark.asyncio
async def test_get_by_reference_dispatches_correctly(
    workflow_state_domain,
    graphql,
    mocker,
) -> None:
    """
    Ensure get_by_reference dispatches to GraphQL.
    """
    result_model = object()
    graphql.get_observation_workflow_state_by_reference = mocker.AsyncMock(
        return_value=result_model
    )

    result = await workflow_state_domain.get_by_reference(
        observation_reference="obs-ref"
    )

    assert result is result_model
    graphql.get_observation_workflow_state_by_reference.assert_called_once_with(
        observation_reference="obs-ref"
    )


def test_check_ready_allows_ready_state() -> None:
    """
    Ensure _check_ready accepts READY workflows.
    """
    workflow = {
        "state": CalculationState.READY.value,
    }

    _check_ready(workflow)


def test_check_ready_raises_for_non_ready_state() -> None:
    """
    Ensure _check_ready raises for non-READY workflows.
    """
    workflow = {
        "state": "PENDING",
    }

    with pytest.raises(RuntimeError):
        _check_ready(workflow)


def test_check_already_set_returns_true_when_matching() -> None:
    """
    Ensure _check_already_set returns true for matching states.
    """
    workflow = {
        "value": {
            "state": ObservationWorkflowState.READY.value,
        }
    }

    assert _check_already_set(workflow, ObservationWorkflowState.READY) is True


def test_check_already_set_returns_false_when_different() -> None:
    """
    Ensure _check_already_set returns false for different states.
    """
    workflow = {
        "value": {
            "state": ObservationWorkflowState.READY.value,
        }
    }

    assert _check_already_set(workflow, ObservationWorkflowState.ONGOING) is False


def test_check_valid_transition_allows_valid_transition() -> None:
    """
    Ensure _check_valid_transition accepts valid transitions.
    """
    workflow = {
        "value": {
            "validTransitions": [ObservationWorkflowState.ONGOING.value],
        }
    }

    _check_valid_transition(workflow, ObservationWorkflowState.ONGOING)


def test_check_valid_transition_raises_for_invalid_transition() -> None:
    """
    Ensure _check_valid_transition raises for invalid transitions.
    """
    workflow = {
        "value": {
            "validTransitions": [ObservationWorkflowState.ONGOING.value],
        }
    }

    with pytest.raises(ValueError):
        _check_valid_transition(workflow, ObservationWorkflowState.INACTIVE)


@pytest.mark.asyncio
async def test_update_by_id_returns_existing_value_when_already_set(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id returns existing workflow when already set.
    """
    workflow_value = {
        "state": ObservationWorkflowState.READY.value,
        "validTransitions": [ObservationWorkflowState.ONGOING.value],
    }
    get_by_id = mocker.patch.object(
        workflow_state_domain,
        "get_by_id",
        return_value={
            "workflow": {"state": CalculationState.READY.value, "value": workflow_value}
        },
    )
    set_state = mocker.patch.object(
        workflow_state_domain._graphql,
        "set_observation_workflow_state",
        new=mocker.AsyncMock(),
    )

    result = await workflow_state_domain.update_by_id(
        observation_id="o-1",
        workflow_state=ObservationWorkflowState.READY,
    )

    assert result == workflow_value
    get_by_id.assert_called_once_with(observation_id="o-1")
    set_state.assert_not_called()


@pytest.mark.asyncio
async def test_update_by_id_sets_new_state_when_valid(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id performs mutation for valid transitions.
    """
    get_by_id = mocker.patch.object(
        workflow_state_domain,
        "get_by_id",
        return_value={
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.READY.value,
                    "validTransitions": [ObservationWorkflowState.ONGOING.value],
                },
            }
        },
    )
    result_model = {"state": ObservationWorkflowState.ONGOING.value}
    set_state = mocker.patch.object(
        workflow_state_domain._graphql,
        "set_observation_workflow_state",
        new=mocker.AsyncMock(return_value=result_model),
    )

    result = await workflow_state_domain.update_by_id(
        observation_id="o-1",
        workflow_state=ObservationWorkflowState.ONGOING,
    )

    assert result == result_model
    get_by_id.assert_called_once_with(observation_id="o-1")
    set_state.assert_called_once_with(
        observation_id="o-1",
        state=ObservationWorkflowState.ONGOING,
    )


@pytest.mark.asyncio
async def test_update_by_id_raises_retryable_error_when_not_ready(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id raises retryable error when calculation is not ready.
    """
    mocker.patch.object(
        workflow_state_domain,
        "get_by_id",
        return_value={
            "workflow": {
                "state": "PENDING",
                "value": {
                    "state": ObservationWorkflowState.READY.value,
                    "validTransitions": [ObservationWorkflowState.ONGOING.value],
                },
            }
        },
    )

    with pytest.raises(GPPRetryableError):
        await workflow_state_domain.update_by_id(
            observation_id="o-1",
            workflow_state=ObservationWorkflowState.ONGOING,
        )


@pytest.mark.asyncio
async def test_update_by_id_raises_validation_error_for_invalid_transition(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id raises validation error for invalid transitions.
    """
    mocker.patch.object(
        workflow_state_domain,
        "get_by_id",
        return_value={
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.READY.value,
                    "validTransitions": [ObservationWorkflowState.ONGOING.value],
                },
            }
        },
    )

    with pytest.raises(GPPValidationError):
        await workflow_state_domain.update_by_id(
            observation_id="o-1",
            workflow_state=ObservationWorkflowState.INACTIVE,
        )


@pytest.mark.asyncio
async def test_update_by_id_with_retry_returns_on_first_success(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id_with_retry returns immediately on success.
    """
    result_model = {"state": ObservationWorkflowState.ONGOING.value}
    update_by_id = mocker.patch.object(
        workflow_state_domain,
        "update_by_id",
        new=mocker.AsyncMock(return_value=result_model),
    )
    sleep = mocker.patch(
        "gpp_client.domains.workflow_state.asyncio.sleep", new=mocker.AsyncMock()
    )

    result = await workflow_state_domain.update_by_id_with_retry(
        observation_id="o-1",
        workflow_state=ObservationWorkflowState.ONGOING,
        max_attempts=3,
        initial_delay=0.0,
        retry_delay=1.0,
    )

    assert result == result_model
    update_by_id.assert_called_once_with(
        observation_id="o-1",
        workflow_state=ObservationWorkflowState.ONGOING,
    )
    sleep.assert_awaited_once_with(0.0)


@pytest.mark.asyncio
async def test_update_by_id_with_retry_retries_then_succeeds(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id_with_retry retries on retryable errors.
    """
    result_model = {"state": ObservationWorkflowState.ONGOING.value}
    update_by_id = mocker.patch.object(
        workflow_state_domain,
        "update_by_id",
        new=mocker.AsyncMock(
            side_effect=[
                GPPRetryableError("not ready"),
                GPPRetryableError("still not ready"),
                result_model,
            ]
        ),
    )
    sleep = mocker.patch(
        "gpp_client.domains.workflow_state.asyncio.sleep", new=mocker.AsyncMock()
    )

    result = await workflow_state_domain.update_by_id_with_retry(
        observation_id="o-1",
        workflow_state=ObservationWorkflowState.ONGOING,
        max_attempts=5,
        initial_delay=0.0,
        retry_delay=1.0,
    )

    assert result == result_model
    assert update_by_id.await_count == 3
    assert sleep.await_args_list == [call(0.0), call(1.0), call(1.0)]


@pytest.mark.asyncio
async def test_update_by_id_with_retry_raises_after_exhausting_attempts(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id_with_retry raises after max retry attempts.
    """
    mocker.patch.object(
        workflow_state_domain,
        "update_by_id",
        new=mocker.AsyncMock(side_effect=GPPRetryableError("not ready")),
    )
    sleep = mocker.patch(
        "gpp_client.domains.workflow_state.asyncio.sleep",
        new=mocker.AsyncMock(),
    )

    with pytest.raises(GPPClientError):
        await workflow_state_domain.update_by_id_with_retry(
            observation_id="o-1",
            workflow_state=ObservationWorkflowState.ONGOING,
            max_attempts=2,
            initial_delay=0.0,
            retry_delay=1.0,
        )

    assert sleep.await_args_list == [call(0.0), call(1.0)]


@pytest.mark.asyncio
async def test_update_by_id_with_retry_raises_validation_error(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id_with_retry re-raises validation errors.
    """
    mocker.patch.object(
        workflow_state_domain,
        "update_by_id",
        new=mocker.AsyncMock(side_effect=GPPValidationError("bad transition")),
    )
    mocker.patch(
        "gpp_client.domains.workflow_state.asyncio.sleep", new=mocker.AsyncMock()
    )

    with pytest.raises(GPPValidationError):
        await workflow_state_domain.update_by_id_with_retry(
            observation_id="o-1",
            workflow_state=ObservationWorkflowState.ONGOING,
        )


@pytest.mark.asyncio
async def test_update_by_id_with_retry_raises_client_error(
    workflow_state_domain,
    mocker,
) -> None:
    """
    Ensure update_by_id_with_retry raises client errors.
    """
    mocker.patch.object(
        workflow_state_domain,
        "update_by_id",
        new=mocker.AsyncMock(side_effect=GPPClientError("client failure")),
    )
    mocker.patch(
        "gpp_client.domains.workflow_state.asyncio.sleep",
        new=mocker.AsyncMock(),
    )

    with pytest.raises(GPPClientError):
        await workflow_state_domain.update_by_id_with_retry(
            observation_id="o-1",
            workflow_state=ObservationWorkflowState.ONGOING,
        )
