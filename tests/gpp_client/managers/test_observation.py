import pytest

from gpp_client.api.enums import Existence
from gpp_client.api.input_types import ObservationPropertiesInput
from gpp_client.exceptions import GPPValidationError
from gpp_client.managers.observation import ObservationManager


@pytest.fixture
def manager(dummy_client) -> ObservationManager:
    """ObservationManager with mocked internal client."""
    return ObservationManager(dummy_client)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "observation_id,observation_reference,should_raise",
    [
        ("abc", None, False),
        (None, "G-2025A-1234-Q-0001", False),
        (None, None, True),
        ("abc", "G-2025A-1234-Q-0001", True),
    ],
)
async def test_clone_requires_exactly_one_identifier(
    manager: ObservationManager,
    observation_id: str | None,
    observation_reference: str | None,
    should_raise: bool,
) -> None:
    """
    Test that ``clone`` requires exactly one observation identifier.
    """
    props = ObservationPropertiesInput()

    if should_raise:
        with pytest.raises(GPPValidationError):
            await manager.clone(
                observation_id=observation_id,
                observation_reference=observation_reference,
                properties=props,
            )
        manager.client.mutation.assert_not_awaited()
        return

    manager.client.mutation.return_value = {"cloneObservation": {"ok": True}}
    result = await manager.clone(
        observation_id=observation_id,
        observation_reference=observation_reference,
        properties=props,
    )
    assert result == {"ok": True}

    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == "cloneObservation"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "program_id,proposal_reference,program_reference,should_raise",
    [
        ("p1", None, None, False),
        (None, "PR-1", None, False),
        (None, None, "G-2025A-Q-123", False),
        (None, None, None, True),
        ("p1", "PR-1", None, True),
        ("p1", None, "G-2025A-Q-123", True),
        (None, "PR-1", "G-2025A-Q-123", True),
        ("p1", "PR-1", "G-2025A-Q-123", True),
    ],
)
async def test_create_requires_exactly_one_program_identifier(
    manager: ObservationManager,
    program_id: str | None,
    proposal_reference: str | None,
    program_reference: str | None,
    should_raise: bool,
) -> None:
    """
    Test that ``create`` requires exactly one program identifier.
    """
    props = ObservationPropertiesInput()

    if should_raise:
        with pytest.raises(GPPValidationError):
            await manager.create(
                properties=props,
                program_id=program_id,
                proposal_reference=proposal_reference,
                program_reference=program_reference,
            )
        manager.client.mutation.assert_not_awaited()
        return

    manager.client.mutation.return_value = {
        "createObservation": {"observation": {"id": "1"}}
    }
    result = await manager.create(
        properties=props,
        program_id=program_id,
        proposal_reference=proposal_reference,
        program_reference=program_reference,
    )
    assert result == {"observation": {"id": "1"}}

    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == "createObservation"

@pytest.mark.parametrize(
    "observation_id,observation_reference,expected_attr,expected_value",
    [
        ("abc", None, "id", "abc"),
        (None, "G-2025A-1234-Q-0001", "reference.label", "G-2025A-1234-Q-0001"),
    ],
)
def test_build_where_for_identifier(
    observation_id: str | None,
    observation_reference: str | None,
    expected_attr: str,
    expected_value: str,
) -> None:
    """
    Test that ``_build_where_for_identifier`` constructs the correct WhereObservation
    based on the provided identifier.
    """
    where = ObservationManager._build_where_for_identifier(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )

    if expected_attr == "id":
        assert where.id.eq == expected_value
        assert where.reference is None
    else:
        assert where.reference.label.eq == expected_value
        assert where.id is None


@pytest.mark.asyncio
async def test_update_by_id_uses_reference_branch(
    mocker, manager: ObservationManager
) -> None:
    """
    Test that ``update_by_id`` uses the reference branch of
    ``_build_where_for_identifier`` when an observation reference is provided.
    """
    manager.update_all = mocker.AsyncMock(return_value={"observations": [{"id": "1"}]})

    spy = mocker.spy(manager, "_build_where_for_identifier")

    ref = "G-2025A-1234-Q-0001"
    result = await manager.update_by_id(
        observation_reference=ref,
        properties=ObservationPropertiesInput(),
        include_deleted=False,
    )

    assert result == {"id": "1"}

    spy.assert_called_once_with(observation_id=None, observation_reference=ref)

    _, kwargs = manager.update_all.await_args
    assert kwargs["limit"] == 1
    assert kwargs["include_deleted"] is False


@pytest.mark.asyncio
async def test_restore_by_id_sets_existence_present(
    mocker, manager: ObservationManager
) -> None:
    """
    Test that ``restore_by_id`` calls ``update_by_id`` with existence set to ``PRESENT``
    and ``include_deleted`` set to ``True``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "1"})

    await manager.restore_by_id(observation_id="abc")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is True
    assert kwargs["properties"].existence == Existence.PRESENT
    assert kwargs["observation_id"] == "abc"


@pytest.mark.asyncio
async def test_delete_by_id_sets_existence_deleted(
    mocker, manager: ObservationManager
) -> None:
    """
    Test that ``delete_by_id`` calls ``update_by_id`` with existence set to ``DELETED``
    and ``include_deleted`` set to ``False``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "1"})

    await manager.delete_by_id(observation_reference="G-2025A-1234-Q-0001")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is False
    assert kwargs["properties"].existence == Existence.DELETED
    assert kwargs["observation_reference"] == "G-2025A-1234-Q-0001"


@pytest.mark.asyncio
async def test_get_by_id_calls_query_with_operation_name(
    manager: ObservationManager,
) -> None:
    """
    Test that ``get_by_id`` calls the client's query method with the correct
    operation name and returns the expected result.
    """
    manager.client.query.return_value = {"observation": {"id": "1"}}

    result = await manager.get_by_id(observation_id="abc")

    assert result == {"id": "1"}
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == "observation"
