from pathlib import Path

import pytest

from gpp_client.mixins.utils import build_input_values, create_program_id_filter


class TestUpdateByIdMixin:
    @pytest.mark.asyncio
    async def test_update_by_id_basic(self, manager, mocker):
        """Test update by identifier dict."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"updated": True}
        )
        identifier = {"programId": "p-test"}
        set_values = {"title": "Updated"}
        expected_input = build_input_values(
            set_values=set_values, identifier=identifier
        )

        query = manager.get_query(query_id="update_by_id")
        result = await manager.update_by_id(
            set_values=set_values, identifier=identifier
        )

        assert result == {"updated": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)

    @pytest.mark.asyncio
    async def test_update_by_id_with_json(self, manager, mocker):
        """Test update by ID using a JSON file to override set values."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"merged": True}
        )
        mocker.patch(
            "gpp_client.mixins.update.merge_set_values", return_value={"merged": True}
        )

        await manager.update_by_id(
            set_values={"initial": True},
            identifier={"programId": "p-test"},
            from_json_file=Path("dummy.json"),
        )

        mock_execute.assert_awaited_once()


class TestUpdateByIdViaBatchMixin:
    @pytest.mark.asyncio
    async def test_update_by_id_via_batch(self, update_by_id_via_batch_manager, mocker):
        """Test update using resource ID in batch mode."""
        mock_execute = mocker.patch.object(
            update_by_id_via_batch_manager, "execute", return_value={"updated": True}
        )
        set_values = {"description": "New"}
        resource_id = "r-test"
        where = {"id": {"EQ": resource_id}}
        expected_input = build_input_values(set_values=set_values, where=where, limit=1)

        query = update_by_id_via_batch_manager.get_query(query_id="update_by_id")
        result = await update_by_id_via_batch_manager.update_by_id(
            resource_id=resource_id, set_values=set_values
        )

        assert result == {"updated": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)


class TestUpdateBatchMixin:
    @pytest.mark.asyncio
    async def test_update_batch(self, manager, mocker):
        """Test updating multiple resources via where clause."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"batch": True}
        )
        set_values = {"flag": True}
        where = {"active": {"EQ": True}}

        expected_input = build_input_values(
            set_values=set_values, where=where, limit=None
        )

        query = manager.get_query(query_id="update_batch")
        result = await manager.update_batch(set_values=set_values, where=where)

        assert result == {"batch": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)


class TestUpdateBatchByProgramIdMixin:
    @pytest.mark.asyncio
    async def test_update_batch_by_program_id(self, manager, mocker):
        """Test batch update with program ID only."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"ok": True}
        )
        program_id = "p-test"
        set_values = {"exists": True}
        program_filter = create_program_id_filter(program_id)

        expected_input = build_input_values(
            set_values=set_values,
            where=program_filter,
            include_deleted=None,
            limit=None,
        )

        query = manager.get_query(query_id="update_batch_by_program_id")
        result = await manager.update_batch_by_program_id(
            program_id=program_id, set_values=set_values
        )

        assert result == {"ok": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)

    @pytest.mark.asyncio
    async def test_update_batch_with_extra_filters(self, manager, mocker):
        """Test update by program ID and extra filter."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"done": True}
        )
        program_id = "p-test"
        extra = {"type": {"EQ": "science"}}
        combined = {"AND": [create_program_id_filter(program_id), extra]}
        set_values = {"x": 1}

        expected_input = build_input_values(
            set_values=set_values, where=combined, limit=25
        )

        query = manager.get_query(query_id="update_batch_by_program_id")
        result = await manager.update_batch_by_program_id(
            program_id=program_id, set_values=set_values, where=extra, limit=25
        )

        assert result == {"done": True}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)
