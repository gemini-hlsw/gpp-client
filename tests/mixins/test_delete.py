import pytest

from gpp_client.mixins.delete import _SET_VALUES
from gpp_client.mixins.utils import build_input_values


class TestDeleteBatchMixin:
    @pytest.mark.asyncio
    async def test_delete_batch(self, manager, mocker):
        """Test that delete_batch calls execute with correct query and input."""
        where = {"status": {"EQ": "inactive"}}
        limit = 5
        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=where,
            limit=limit,
            include_deleted=False,
        )

        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"deleted": True}
        )
        query = manager.get_query(query_id="delete_batch")

        result = await manager.delete_batch(where=where, limit=limit)
        assert result == {"deleted": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)


class TestDeleteByIdViaBatchMixin:
    @pytest.mark.asyncio
    async def test_delete_by_id(self, manager, mocker):
        """Test that delete_by_id constructs the correct where clause."""
        resource_id = "n-abc123"
        expected_where = {"id": {"EQ": resource_id}}
        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=expected_where,
            limit=1,
            include_deleted=False,
        )

        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"deleted": True}
        )
        query = manager.get_query(query_id="delete_by_id")

        result = await manager.delete_by_id(resource_id=resource_id)
        assert result == {"deleted": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)


class TestDeleteBatchByProgramIdMixin:
    @pytest.mark.asyncio
    async def test_delete_batch_by_program_id_only(self, manager, mocker):
        """Test deletion with only program_id (no additional filters)."""
        program_id = "p-test"
        expected_where = {"program": {"id": {"EQ": program_id}}}
        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=expected_where,
            limit=None,
            include_deleted=False,
        )

        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"deleted": True}
        )
        query = manager.get_query(query_id="delete_batch_by_program_id")

        result = await manager.delete_batch_by_program_id(program_id=program_id)
        assert result == {"deleted": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)

    @pytest.mark.asyncio
    async def test_delete_batch_by_program_id_with_filter(self, manager, mocker):
        """Test deletion with program_id and additional ANDed filter."""
        program_id = "p-test"
        extra_where = {"status": {"EQ": "expired"}}
        expected_where = {
            "AND": [
                {"program": {"id": {"EQ": program_id}}},
                extra_where,
            ]
        }

        expected_input = build_input_values(
            set_values=_SET_VALUES,
            where=expected_where,
            limit=None,
            include_deleted=False,
        )

        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"deleted": True}
        )
        query = manager.get_query(query_id="delete_batch_by_program_id")

        result = await manager.delete_batch_by_program_id(
            program_id=program_id, where=extra_where
        )
        assert result == {"deleted": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)
