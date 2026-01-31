import pytest

from gpp_client.api.enums import Existence
from gpp_client.api.input_types import ProgramNotePropertiesInput
from gpp_client.managers.program_note import ProgramNoteManager


@pytest.fixture
def manager(dummy_client) -> ProgramNoteManager:
    """ProgramNoteManager with mocked internal client."""
    return ProgramNoteManager(dummy_client)


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
    manager: ProgramNoteManager,
    program_id: str | None,
    proposal_reference: str | None,
    program_reference: str | None,
    should_raise: bool,
) -> None:
    """
    Test that ``create`` requires exactly one program identifier.
    """
    props = ProgramNotePropertiesInput()

    if should_raise:
        # Validation error type comes from BaseManager.raise_error => GPPValidationError.
        from gpp_client.exceptions import GPPValidationError

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
        "createProgramNote": {"programNote": {"id": "1"}}
    }

    result = await manager.create(
        properties=props,
        program_id=program_id,
        proposal_reference=proposal_reference,
        program_reference=program_reference,
    )

    assert result == {"programNote": {"id": "1"}}
    _, kwargs = manager.client.mutation.await_args
    assert kwargs["operation_name"] == "createProgramNote"


def test_build_where_for_id() -> None:
    """
    Test that ``_build_where_for_id`` constructs the correct ``WhereProgramNote``
    filter.
    """
    where = ProgramNoteManager._build_where_for_id(program_note_id="pn-1")
    assert where.id.eq == "pn-1"


@pytest.mark.asyncio
async def test_update_by_id_builds_where_and_limits_one(
    mocker, manager: ProgramNoteManager
) -> None:
    """
    Test that ``update_by_id`` builds the correct ``WhereProgramNote`` filter and
    sets the limit to 1.
    """
    manager.update_all = mocker.AsyncMock(return_value={"programNotes": [{"id": "1"}]})

    spy = mocker.spy(manager, "_build_where_for_id")

    result = await manager.update_by_id(
        "pn-1",
        properties=ProgramNotePropertiesInput(),
        include_deleted=True,
    )

    assert result == {"id": "1"}
    spy.assert_called_once_with(program_note_id="pn-1")

    _, kwargs = manager.update_all.await_args
    assert kwargs["limit"] == 1
    assert kwargs["include_deleted"] is True
    assert kwargs["where"].id.eq == "pn-1"


@pytest.mark.asyncio
async def test_restore_by_id_sets_existence_present(
    mocker, manager: ProgramNoteManager
) -> None:
    """
    Test that ``restore_by_id`` calls ``update_by_id`` with existence set to ``PRESENT``
    and ``include_deleted`` set to ``True``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "1"})

    await manager.restore_by_id("pn-1")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is True
    assert kwargs["properties"].existence == Existence.PRESENT


@pytest.mark.asyncio
async def test_delete_by_id_sets_existence_deleted(
    mocker, manager: ProgramNoteManager
) -> None:
    """
    Test that ``delete_by_id`` calls ``update_by_id`` with existence set to ``DELETED``
    and ``include_deleted`` set to ``False``.
    """
    manager.update_by_id = mocker.AsyncMock(return_value={"id": "1"})

    await manager.delete_by_id("pn-1")

    _, kwargs = manager.update_by_id.await_args
    assert kwargs["include_deleted"] is False
    assert kwargs["properties"].existence == Existence.DELETED


@pytest.mark.asyncio
async def test_get_by_id_calls_query_with_operation_name(
    manager: ProgramNoteManager,
) -> None:
    """
    Test that ``get_by_id`` calls ``client.query`` with the correct operation name.
    """
    manager.client.query.return_value = {"programNote": {"id": "1"}}

    result = await manager.get_by_id("pn-1")

    assert result == {"id": "1"}
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == "programNote"
