import pytest

from gpp_client.api.enums import ConfigurationRequestStatus
from gpp_client.api.input_types import WhereConfigurationRequest
from gpp_client.managers.configuration_request import ConfigurationRequestManager


@pytest.fixture
def manager(dummy_client) -> ConfigurationRequestManager:
    """ConfigurationRequestManager with mocked internal client."""
    return ConfigurationRequestManager(dummy_client)


def test_build_where_none_returns_new_model() -> None:
    """
    Test that ``_build_where`` returns a new WhereConfigurationRequest when no
    base model is provided.
    """
    where = ConfigurationRequestManager._build_where(
        program_id=None,
        status=None,
        where=None,
    )

    assert isinstance(where, WhereConfigurationRequest)


def test_build_where_copies_model_when_provided() -> None:
    """
    Test that ``_build_where`` copies the provided model instead of mutating it.
    """
    base = WhereConfigurationRequest()

    built = ConfigurationRequestManager._build_where(
        program_id=None,
        status=None,
        where=base,
    )

    assert built is not base
    assert built == base


def test_build_where_applies_program_id_override() -> None:
    """
    Test that ``_build_where`` applies the program_id override.
    """
    built = ConfigurationRequestManager._build_where(
        program_id="p-1",
        status=None,
        where=None,
    )

    assert built.program.id.eq == "p-1"


def test_build_where_applies_status_override() -> None:
    """
    Test that ``_build_where`` applies the status override.
    """
    built = ConfigurationRequestManager._build_where(
        program_id=None,
        status=ConfigurationRequestStatus.APPROVED,
        where=None,
    )

    assert built.status.eq == ConfigurationRequestStatus.APPROVED


def test_build_where_applies_both_overrides_and_does_not_mutate_base() -> None:
    """
    Test that ``_build_where`` applies both overrides and does not mutate the input model.
    """
    base = WhereConfigurationRequest()

    built = ConfigurationRequestManager._build_where(
        program_id="p-9",
        status=ConfigurationRequestStatus.APPROVED,
        where=base,
    )

    assert built is not base
    assert built.program.id.eq == "p-9"
    assert built.status.eq == ConfigurationRequestStatus.APPROVED

    # Base remains unchanged (no mutation).
    assert base.program is None
    assert base.status is None


@pytest.mark.asyncio
async def test_get_all_calls_query_with_operation_name_and_returns_payload(
    manager: ConfigurationRequestManager,
) -> None:
    """
    Test that ``get_all`` calls the client's query with the correct operation name
    and returns the unwrapped payload.
    """
    manager.client.query.return_value = {
        ConfigurationRequestManager._OP_LIST: {"hasMore": False, "matches": []}
    }

    result = await manager.get_all(offset=10, limit=5)

    assert result == {"hasMore": False, "matches": []}

    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == ConfigurationRequestManager._OP_LIST


@pytest.mark.asyncio
async def test_get_all_approved_by_program_id_delegates_to_get_all(
    mocker, manager: ConfigurationRequestManager
) -> None:
    """
    Test that ``get_all_approved_by_program_id`` delegates to ``get_all`` with
    the expected status and program_id.
    """
    manager.get_all = mocker.AsyncMock(return_value={"hasMore": False, "matches": []})

    result = await manager.get_all_approved_by_program_id(program_id="p-2")

    assert result == {"hasMore": False, "matches": []}

    _, kwargs = manager.get_all.await_args
    assert kwargs["program_id"] == "p-2"
    assert kwargs["status"] == ConfigurationRequestStatus.APPROVED
