import pytest

from gpp_client.api.enums import Existence
from gpp_client.api.input_types import CallForProposalsPropertiesInput
from gpp_client.managers.call_for_proposals import CallForProposalsManager


@pytest.fixture
def manager(dummy_client) -> CallForProposalsManager:
    """CallForProposalsManager with mocked internal client."""
    return CallForProposalsManager(dummy_client)


@pytest.mark.asyncio
async def test_create_calls_mutation_with_operation_name_and_returns_payload(
    manager: CallForProposalsManager,
) -> None:
    """
    Test that ``create`` calls the client's mutation method with the correct
    operation name and returns the expected payload.
    """
    manager.client.mutation.return_value = {
        CallForProposalsManager._OP_CREATE: {"callForProposals": {"id": "cfp-1"}}
    }

    result = await manager.create(properties=CallForProposalsPropertiesInput())

    assert result == {"callForProposals": {"id": "cfp-1"}}

    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == CallForProposalsManager._OP_CREATE


def test_build_where_for_id_constructs_expected_filter() -> None:
    """
    Test that ``_build_where_for_id`` constructs the expected filter.
    """
    where = CallForProposalsManager._build_where_for_id(call_for_proposals_id="cfp-9")
    assert where.id.eq == "cfp-9"


@pytest.mark.asyncio
async def test_update_by_id_delegates_to_update_all_and_extracts_single_item(
    mocker, manager: CallForProposalsManager
) -> None:
    """
    Test that ``update_by_id`` delegates to ``update_all`` with the correct
    parameters and extracts the single call for proposals from the result.
    """
    manager.update_all = mocker.AsyncMock(
        return_value={CallForProposalsManager._OP_LIST: [{"id": "cfp-1"}]}
    )
    spy = mocker.spy(manager, "_build_where_for_id")

    result = await manager.update_by_id(
        "cfp-1",
        properties=CallForProposalsPropertiesInput(),
        include_deleted=False,
    )

    assert result == {"id": "cfp-1"}

    spy.assert_called_once_with(call_for_proposals_id="cfp-1")

    _, kwargs = manager.update_all.await_args
    assert kwargs["limit"] == 1
    assert kwargs["include_deleted"] is False


@pytest.mark.asyncio
async def test_restore_by_id_sets_existence_present_and_include_deleted_true(
    mocker, manager: CallForProposalsManager
) -> None:
    """
    Test that ``restore_by_id`` calls ``update_by_id`` with existence set to PRESENT
    and ``include_deleted`` set to True.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "cfp-1"})

    await manager.restore_by_id("cfp-1")

    args, kwargs = manager.update_by_id.await_args
    assert args[0] == "cfp-1"
    assert kwargs["include_deleted"] is True
    assert kwargs["properties"].existence == Existence.PRESENT


@pytest.mark.asyncio
async def test_delete_by_id_sets_existence_deleted_and_include_deleted_false(
    mocker, manager: CallForProposalsManager
) -> None:
    """
    Test that ``delete_by_id`` calls ``update_by_id`` with existence set to DELETED
    and ``include_deleted`` set to False.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "cfp-1"})

    await manager.delete_by_id("cfp-1")

    args, kwargs = manager.update_by_id.await_args
    assert args[0] == "cfp-1"
    assert kwargs["include_deleted"] is False
    assert kwargs["properties"].existence == Existence.DELETED


@pytest.mark.asyncio
async def test_get_by_id_calls_query_with_operation_name_and_returns_result(
    manager: CallForProposalsManager,
) -> None:
    """
    Test that ``get_by_id`` calls the query with the correct operation name
    and returns the expected result.
    """
    manager.client.query.return_value = {
        CallForProposalsManager._OP_GET: {"id": "cfp-1"}
    }

    result = await manager.get_by_id("cfp-1")

    assert result == {"id": "cfp-1"}

    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == CallForProposalsManager._OP_GET


@pytest.mark.asyncio
async def test_get_all_calls_query_with_operation_name_and_returns_result(
    manager: CallForProposalsManager,
) -> None:
    """
    Test that ``get_all`` calls the query with the correct operation name
    and returns the expected result.
    """
    manager.client.query.return_value = {
        CallForProposalsManager._OP_LIST: {"hasMore": False, "matches": []}
    }

    result = await manager.get_all(include_deleted=True, offset=10, limit=5)

    assert result == {"hasMore": False, "matches": []}

    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == CallForProposalsManager._OP_LIST
