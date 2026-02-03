import pytest

from gpp_client.api.enums import Existence
from gpp_client.api.input_types import ProgramPropertiesInput
from gpp_client.managers.program import ProgramManager


@pytest.fixture
def manager(dummy_client) -> ProgramManager:
    """ProgramManager with mocked internal client."""
    return ProgramManager(dummy_client)


def test_build_where_for_id_constructs_expected_filter() -> None:
    """
    Test that ``_build_where_for_id`` constructs the expected filter.
    """
    where = ProgramManager._build_where_for_id(program_id="p1")
    assert where.id.eq == "p1"


@pytest.mark.asyncio
async def test_create_calls_mutation_with_operation_name_and_returns_payload(
    manager: ProgramManager,
) -> None:
    """
    Test that ``create`` calls mutation with correct operation name
    and returns the expected payload.
    """
    manager.client.mutation.return_value = {
        ProgramManager._OP_CREATE: {"program": {"id": "p1"}}
    }

    result = await manager.create(properties=ProgramPropertiesInput())

    assert result == {"program": {"id": "p1"}}
    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == ProgramManager._OP_CREATE


@pytest.mark.asyncio
async def test_update_all_calls_mutation_with_operation_name_and_returns_payload(
    manager: ProgramManager,
) -> None:
    """
    Test that ``update_all`` calls mutation with correct operation name
    and returns the expected payload.
    """
    manager.client.mutation.return_value = {
        ProgramManager._OP_UPDATE: {"hasMore": False, "programs": []}
    }

    result = await manager.update_all(properties=ProgramPropertiesInput())

    assert result == {"hasMore": False, "programs": []}
    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == ProgramManager._OP_UPDATE


@pytest.mark.asyncio
async def test_update_by_id_builds_where_and_limits_to_one(
    mocker,
    manager: ProgramManager,
) -> None:
    """
    Test that ``update_by_id`` builds the correct ``where`` filter and limits
    the update to one program.
    """
    manager.update_all = mocker.AsyncMock(return_value={"programs": [{"id": "p1"}]})

    spy = mocker.spy(ProgramManager, "_build_where_for_id")

    result = await manager.update_by_id(
        "p1",
        properties=ProgramPropertiesInput(),
        include_deleted=True,
    )

    assert result == {"id": "p1"}
    spy.assert_called_once_with(program_id="p1")

    _, kwargs = manager.update_all.await_args
    assert kwargs["limit"] == 1
    assert kwargs["include_deleted"] is True

    where = kwargs["where"]
    assert where.id.eq == "p1"


@pytest.mark.asyncio
async def test_get_by_id_calls_query_with_operation_name_and_returns_payload(
    manager: ProgramManager,
) -> None:
    """
    Test that ``get_by_id`` calls query with correct operation name
    and returns the expected payload.
    """
    manager.client.query.return_value = {ProgramManager._OP_GET: {"id": "p1"}}

    result = await manager.get_by_id("p1")

    assert result == {"id": "p1"}
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == ProgramManager._OP_GET


@pytest.mark.asyncio
async def test_get_all_calls_query_with_operation_name_and_returns_payload(
    manager: ProgramManager,
) -> None:
    """
    Test that ``get_all`` calls query with correct operation name
    and returns the expected payload.
    """
    manager.client.query.return_value = {
        ProgramManager._OP_LIST: {"hasMore": False, "matches": []}
    }

    result = await manager.get_all()

    assert result == {"hasMore": False, "matches": []}
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == ProgramManager._OP_LIST


@pytest.mark.asyncio
async def test_restore_by_id_sets_existence_present_and_include_deleted_true(
    mocker,
    manager: ProgramManager,
) -> None:
    """
    Test that ``restore_by_id`` sets ``existence`` to ``PRESENT`` and
    ``include_deleted`` to ``True``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "p1"})

    await manager.restore_by_id("p1")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is True
    assert kwargs["properties"].existence == Existence.PRESENT


@pytest.mark.asyncio
async def test_delete_by_id_sets_existence_deleted_and_include_deleted_false(
    mocker,
    manager: ProgramManager,
) -> None:
    """
    Test that ``delete_by_id`` sets ``existence`` to ``DELETED`` and
    ``include_deleted`` to ``False``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "p1"})

    await manager.delete_by_id("p1")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is False
    assert kwargs["properties"].existence == Existence.DELETED
