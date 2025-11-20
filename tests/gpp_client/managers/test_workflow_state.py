import pytest  # type: ignore

from gpp_client.api.enums import CalculationState, ObservationWorkflowState
from gpp_client.exceptions import GPPValidationError
from gpp_client.managers.workflow_state import WorkflowStateManager


@pytest.fixture
def workflow_state_manager(mocker):
    """Fixture to create a WorkflowStateManager with a mocked client."""
    mock_client = mocker.AsyncMock()
    return WorkflowStateManager(client=mock_client)


@pytest.mark.asyncio
async def test_get_by_id_with_observation_id(workflow_state_manager):
    """Test fetching workflow state by observation ID."""
    mock_client = workflow_state_manager.client
    mock_result = {
        "observation": {
            "id": "o-145",
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.DEFINED.value,
                    "validTransitions": [ObservationWorkflowState.INACTIVE.value],
                    "validationErrors": [],
                },
            },
        }
    }
    mock_client.query.return_value = mock_result

    result = await workflow_state_manager.get_by_id(observation_id="o-145")

    assert result == mock_result["observation"], (
        "The returned observation does not match the expected result."
    )
    mock_client.query.assert_called_once()


@pytest.mark.asyncio
async def test_get_by_id_with_observation_reference(workflow_state_manager):
    """Test fetching workflow state by observation reference."""
    mock_client = workflow_state_manager.client
    mock_result = {
        "observation": {
            "id": "o-145",
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.DEFINED.value,
                    "validTransitions": [ObservationWorkflowState.INACTIVE.value],
                    "validationErrors": [],
                },
            },
        }
    }
    mock_client.query.return_value = mock_result

    result = await workflow_state_manager.get_by_id(observation_reference="obs-ref")

    assert result == mock_result["observation"], (
        "The returned observation does not match the expected result."
    )
    mock_client.query.assert_called_once()


@pytest.mark.asyncio
async def test_update_by_id_valid_transition(workflow_state_manager):
    """Test updating workflow state with a valid transition."""
    mock_client = workflow_state_manager.client
    mock_get_result = {
        "observation": {
            "id": "o-145",
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.DEFINED.value,
                    "validTransitions": [ObservationWorkflowState.INACTIVE.value],
                    "validationErrors": [],
                },
            },
        }
    }
    mock_client.query.return_value = mock_get_result
    mock_client.mutation.return_value = {
        "setObservationWorkflowState": {
            "state": ObservationWorkflowState.INACTIVE.value
        }
    }

    result = await workflow_state_manager.update_by_id(
        workflow_state=ObservationWorkflowState.INACTIVE, observation_id="o-145"
    )

    assert result == {"state": ObservationWorkflowState.INACTIVE.value}, (
        "The workflow state was not updated correctly."
    )
    mock_client.query.assert_called_once()
    mock_client.mutation.assert_called_once()


@pytest.mark.asyncio
async def test_update_by_id_invalid_transition(workflow_state_manager):
    """Test updating workflow state with an invalid transition."""
    mock_client = workflow_state_manager.client
    mock_get_result = {
        "observation": {
            "id": "o-145",
            "workflow": {
                "state": CalculationState.READY.value,
                "value": {
                    "state": ObservationWorkflowState.DEFINED.value,
                    "validTransitions": [ObservationWorkflowState.INACTIVE.value],
                    "validationErrors": [],
                },
            },
        }
    }
    mock_client.query.return_value = mock_get_result

    with pytest.raises(GPPValidationError):
        await workflow_state_manager.update_by_id(
            workflow_state=ObservationWorkflowState.ONGOING, observation_id="o-145"
        )

    mock_client.query.assert_called_once()
    mock_client.mutation.assert_not_called()


@pytest.mark.parametrize(
    "workflow, should_raise",
    [
        ({"state": CalculationState.READY.value}, False),
        ({"state": CalculationState.PENDING.value}, True),
        ({"state": CalculationState.CALCULATING.value}, True),
        ({"state": CalculationState.RETRY.value}, True),
    ],
)
def test_check_ready(workflow: dict[str, str], should_raise: bool) -> None:
    """Test _check_ready for correct RuntimeError behavior."""
    if should_raise:
        with pytest.raises(RuntimeError):
            WorkflowStateManager._check_ready(workflow)
    else:
        WorkflowStateManager._check_ready(workflow)


@pytest.mark.parametrize(
    "workflow, workflow_state, expected",
    [
        (
            {"value": {"state": ObservationWorkflowState.DEFINED.value}},
            ObservationWorkflowState.DEFINED,
            True,
        ),
        (
            {"value": {"state": ObservationWorkflowState.INACTIVE.value}},
            ObservationWorkflowState.DEFINED,
            False,
        ),
    ],
)
def test_check_already_set(
    workflow: dict[str, dict[str, str]],
    workflow_state: ObservationWorkflowState,
    expected: bool,
) -> None:
    """Test _check_already_set correctly matches state equality."""
    result = WorkflowStateManager._check_already_set(workflow, workflow_state)
    assert result is expected


@pytest.mark.parametrize(
    "workflow, workflow_state, should_raise",
    [
        (
            {"value": {"validTransitions": ["READY", "DEFINED"]}},
            ObservationWorkflowState.DEFINED,
            False,
        ),
        (
            {"value": {"validTransitions": ["INACTIVE"]}},
            ObservationWorkflowState.DEFINED,
            True,
        ),
        ({"value": {"validTransitions": []}}, ObservationWorkflowState.DEFINED, True),
        ({"value": {}}, ObservationWorkflowState.INACTIVE, True),
    ],
)
def test_check_valid_transition(
    workflow: dict[str, dict[str, list[str]]],
    workflow_state: ObservationWorkflowState,
    should_raise: bool,
) -> None:
    """Test _check_valid_transition for valid and invalid transitions."""
    if should_raise:
        with pytest.raises(ValueError):
            WorkflowStateManager._check_valid_transition(workflow, workflow_state)
    else:
        WorkflowStateManager._check_valid_transition(workflow, workflow_state)
