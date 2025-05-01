import pytest

from gpp_client.mixins.restore import _SET_VALUES
from gpp_client.mixins.utils import build_input_values, create_program_id_filter


class TestRestoreByIdViaBatchMixin:
    @pytest.mark.asyncio
    async def test_restore_by_id(self, manager, mocker):
        """Test restoring a single resource by ID."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"restored": True}
        )
        resource_id = "r-test"
        where = {"id": {"EQ": resource_id}}
        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=where,
            limit=1,
            include_deleted=True,
        )
        query = manager.get_query(query_id="restore_by_id")
        result = await manager.restore_by_id(resource_id=resource_id)

        assert result == {"restored": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)


class TestRestoreBatchByProgramIdMixin:
    @pytest.mark.asyncio
    async def test_restore_batch_by_program_id(self, manager, mocker):
        """Test restoring resources with only a program ID."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"batch": True}
        )
        program_id = "p-test"
        program_filter = create_program_id_filter(program_id)

        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=program_filter,
            limit=None,
            include_deleted=True,
        )
        query = manager.get_query(query_id="restore_batch_by_program_id")
        result = await manager.restore_batch_by_program_id(program_id=program_id)

        assert result == {"batch": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)

    @pytest.mark.asyncio
    async def test_restore_batch_with_additional_filters(self, manager, mocker):
        """Test restoring with program ID and additional filters."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"combined": True}
        )
        program_id = "p-test"
        extra_where = {"status": {"EQ": "archived"}}
        combined = {"AND": [create_program_id_filter(program_id), extra_where]}

        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=combined,
            limit=25,
            include_deleted=True,
        )
        query = manager.get_query(query_id="restore_batch_by_program_id")
        result = await manager.restore_batch_by_program_id(
            program_id=program_id,
            where=extra_where,
            limit=25,
        )

        assert result == {"combined": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)
