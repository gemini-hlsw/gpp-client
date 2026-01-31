import pytest

from gpp_client.api.enums import Existence
from gpp_client.api.input_types import TargetPropertiesInput
from gpp_client.exceptions import GPPValidationError
from gpp_client.managers.target import TargetManager


@pytest.fixture
def manager(dummy_client) -> TargetManager:
    """TargetManager with mocked internal client."""
    return TargetManager(dummy_client)


@pytest.mark.asyncio
async def test_clone_calls_mutation_with_operation_name_and_returns_payload(
    manager: TargetManager,
) -> None:
    """
    ￼Test that ``clone`` calls the client's mutation method with the
    correct operation name and returns the expected payload.
    """
    manager.client.mutation.return_value = {
        TargetManager._OP_CLONE: {
            "originalTarget": {"id": "t-1"},
            "newTarget": {"id": "t-2"},
        }
    }

    result = await manager.clone(target_id="t-1", properties=TargetPropertiesInput())

    assert result == {
        "originalTarget": {"id": "t-1"},
        "newTarget": {"id": "t-2"},
    }

    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == TargetManager._OP_CLONE


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
    manager: TargetManager,
    program_id: str | None,
    proposal_reference: str | None,
    program_reference: str | None,
    should_raise: bool,
) -> None:
    """
    Test that ``create`` requires exactly one program identifier and
    behaves accordingly.
    """
    props = TargetPropertiesInput()

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
        TargetManager._OP_CREATE: {"target": {"id": "t-1"}}
    }

    result = await manager.create(
        properties=props,
        program_id=program_id,
        proposal_reference=proposal_reference,
        program_reference=program_reference,
    )

    assert result == {"target": {"id": "t-1"}}

    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == TargetManager._OP_CREATE


def test_build_where_for_id_constructs_expected_filter() -> None:
    """
    Test that ``_build_where_for_id`` constructs the expected filter.
    """
    where = TargetManager._build_where_for_id(target_id="t-123")
    assert where.id.eq == "t-123"


@pytest.mark.asyncio
async def test_update_by_id_delegates_to_update_all_and_extracts_single_target(
    mocker, manager: TargetManager
) -> None:
    """
    Test that ``update_by_id`` delegates to ``update_all`` with the correct
    parameters and extracts the single target from the result.
    """
    manager.update_all = mocker.AsyncMock(
        return_value={TargetManager._OP_LIST: [{"id": "t-1"}]}
    )
    spy = mocker.spy(manager, "_build_where_for_id")

    result = await manager.update_by_id("t-1", properties=TargetPropertiesInput())

    assert result == {"id": "t-1"}
    spy.assert_called_once_with(target_id="t-1")

    _, kwargs = manager.update_all.await_args
    assert kwargs["limit"] == 1
    assert kwargs["include_deleted"] is False


@pytest.mark.asyncio
async def test_restore_by_id_sets_existence_present_and_include_deleted_true(
    mocker, manager: TargetManager
) -> None:
    """
    Test that ``restore_by_id`` sets the correct existence and
    include_deleted parameters when calling ``update_by_id``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "t-1"})

    await manager.restore_by_id("t-1")

    args, kwargs = manager.update_by_id.await_args
    assert args[0] == "t-1"
    assert kwargs["include_deleted"] is True
    assert kwargs["properties"].existence == Existence.PRESENT


@pytest.mark.asyncio
async def test_delete_by_id_sets_existence_deleted_and_include_deleted_false(
    mocker, manager: TargetManager
) -> None:
    """
    Test that ``delete_by_id`` sets the correct existence and
    include_deleted parameters when calling ``update_by_id``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "t-1"})

    await manager.delete_by_id("t-1")

    args, kwargs = manager.update_by_id.await_args
    assert args[0] == "t-1"
    assert kwargs["include_deleted"] is False
    assert kwargs["properties"].existence == Existence.DELETED


@pytest.mark.asyncio
async def test_get_by_id_calls_query_with_operation_name_and_returns_result(
    manager: TargetManager,
) -> None:
    """
    Test that ``get_by_id`` calls the query with the correct operation name
    and returns the expected result.
    """
    manager.client.query.return_value = {TargetManager._OP_GET: {"id": "t-1"}}

    result = await manager.get_by_id("t-1")

    assert result == {"id": "t-1"}

    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == TargetManager._OP_GET


@pytest.mark.asyncio
async def test_get_all_calls_query_with_operation_name(
    manager: TargetManager,
) -> None:
    """
    Test that ``get_all`` calls the query with the correct operation name
    and returns the expected result.
    """
    manager.client.query.return_value = {
        TargetManager._OP_LIST: {"hasMore": False, "matches": []}
    }

    result = await manager.get_all(include_deleted=True, offset=10, limit=5)

    assert result == {"hasMore": False, "matches": []}

    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == TargetManager._OP_LIST
