import pytest

from gpp_client.mixins.utils import build_selector_values


class TestGetByIdMixin:
    @pytest.mark.asyncio
    async def test_get_by_id_valid(self, manager, mocker):
        """Test get_by_id with standard ID input."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"ok": True}
        )
        result = await manager.get_by_id(resource_id="abc")
        assert result == {"ok": True}
        mock_execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_by_id_with_identifier_dict(self, manager, mocker):
        """Test advanced usage with identifier dictionary."""
        identifier = {"otherId": "x"}
        expected_selectors = build_selector_values(identifier=identifier)
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"ok": True}
        )
        query = manager.get_query(query_id="get_by_id")
        result = await manager.get_by_id(_identifier=identifier)
        assert result == {"ok": True}
        mock_execute.assert_awaited_once_with(
            query=query, selector_values=expected_selectors
        )

    @pytest.mark.asyncio
    async def test_get_by_id_raises_on_missing_input(self, manager):
        """Ensure get_by_id raises if neither ID nor identifier is given."""
        with pytest.raises(ValueError):
            await manager.get_by_id()  # Must await


class TestGetBatchMixin:
    @pytest.mark.asyncio
    async def test_get_batch_with_filters(self, manager, mocker):
        """Test get_batch applies correct filters and fields."""
        where = {"status": {"EQ": "active"}}
        expected_selectors = build_selector_values(
            where=where, limit=10, include_deleted=True
        )
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"batch": True}
        )
        query = manager.get_query(query_id="get_batch")
        result = await manager.get_batch(where=where, limit=10, include_deleted=True)
        assert result == {"batch": True}
        mock_execute.assert_awaited_once_with(
            query=query, selector_values=expected_selectors
        )


class TestGetBatchByProgramIdMixin:
    @pytest.mark.asyncio
    async def test_get_batch_by_program_id(self, manager, mocker):
        """Test basic query for program ID only."""
        program_id = "p-xyz"
        expected_selectors = build_selector_values(
            where={"program": {"id": {"EQ": program_id}}}
        )
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"data": True}
        )
        query = manager.get_query(query_id="get_batch_by_program_id")
        result = await manager.get_batch_by_program_id(program_id=program_id)
        assert result == {"data": True}
        mock_execute.assert_awaited_once_with(
            query=query, selector_values=expected_selectors
        )

    @pytest.mark.asyncio
    async def test_get_batch_by_program_id_with_extra_filters(self, manager, mocker):
        """Test query for program ID and extra where clause."""
        program_id = "p-123"
        extra_where = {"status": {"EQ": "closed"}}
        combined = {"AND": [{"program": {"id": {"EQ": program_id}}}, extra_where]}
        expected_selectors = build_selector_values(where=combined)

        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"ok": True}
        )
        query = manager.get_query(query_id="get_batch_by_program_id")
        result = await manager.get_batch_by_program_id(
            program_id=program_id, where=extra_where
        )
        assert result == {"ok": True}
        mock_execute.assert_awaited_once_with(
            query=query, selector_values=expected_selectors
        )
