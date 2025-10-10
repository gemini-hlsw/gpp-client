import pytest

from gpp_client.api.enums import CalculationState, ObservationWorkflowState
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

    with pytest.raises(ValueError):
        await workflow_state_manager.update_by_id(
            workflow_state=ObservationWorkflowState.ONGOING, observation_id="o-145"
        )

    mock_client.query.assert_called_once()
    mock_client.mutation.assert_not_called()


@pytest.mark.parametrize(
    "workflow, desired_state, expected, message",
    [
        # Case: Transition allowed.
        (
            {
                "state": CalculationState.READY.value,
                "value": {
                    "validTransitions": [
                        ObservationWorkflowState.INACTIVE.value,
                        ObservationWorkflowState.DEFINED.value,
                    ]
                },
            },
            ObservationWorkflowState.INACTIVE,
            True,
            "Transition to 'INACTIVE' should be allowed when in 'READY' state.",
        ),
        # Case: Transition not allowed.
        (
            {
                "state": CalculationState.READY.value,
                "value": {
                    "validTransitions": [
                        ObservationWorkflowState.INACTIVE.value,
                        ObservationWorkflowState.DEFINED.value,
                    ]
                },
            },
            ObservationWorkflowState.ONGOING,
            False,
            "Transition to 'ONGOING' should not be allowed when not in valid transitions.",
        ),
        # Case: State not READY.
        (
            {
                "state": CalculationState.PENDING.value,
                "value": {
                    "validTransitions": [
                        ObservationWorkflowState.INACTIVE.value,
                        ObservationWorkflowState.DEFINED.value,
                    ]
                },
            },
            ObservationWorkflowState.INACTIVE,
            False,
            "Transition should not be allowed when state is not 'READY'.",
        ),
        # Case: No valid transitions.
        (
            {
                "state": CalculationState.READY.value,
                "value": {"validTransitions": []},
            },
            ObservationWorkflowState.INACTIVE,
            False,
            "Transition should not be allowed when there are no valid transitions.",
        ),
        # Case: Missing validTransitions key.
        (
            {
                "state": CalculationState.READY.value,
                "value": {},
            },
            ObservationWorkflowState.INACTIVE,
            False,
            "Transition should not be allowed when 'validTransitions' key is missing.",
        ),
    ],
)
def test_can_transition_to(workflow, desired_state, expected, message):
    """Test the `_can_transition_to` static method with various scenarios."""
    result = WorkflowStateManager._can_transition_to(desired_state, workflow)
    assert result == expected, message
