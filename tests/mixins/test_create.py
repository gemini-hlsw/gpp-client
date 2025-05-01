from pathlib import Path

import pytest

from gpp_client.mixins.utils import build_input_values


class TestCreateMixin:
    def test_get_query_is_resolved(self, manager):
        """Ensure get_query uses correct query_id and substitutes fields."""
        query = manager.get_query(query_id="create", fields="id title")
        assert "id title" in query
        assert "mutation" in query

    @pytest.mark.asyncio
    async def test_create_successful(self, manager, mocker):
        """Test a successful create request returns the correct response."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"created": "ok"}
        )
        query = manager.get_query(query_id="create")

        result = await manager.create(set_values={"title": "Test"})
        expected_input = build_input_values(set_values={"title": "Test"})

        assert result == {"created": "ok"}
        mock_execute.assert_awaited_once_with(query=query, input_values=expected_input)

    @pytest.mark.asyncio
    async def test_create_with_identifier(self, manager, mocker):
        """Test create supports identifier merging."""
        mock_execute = mocker.patch.object(
            manager, "execute", return_value={"created": "ok"}
        )
        identifier = {"programId": "p-123"}

        await manager.create(set_values={"title": "X"}, identifier=identifier)

        expected_input = build_input_values(
            set_values={"title": "X"}, identifier=identifier
        )
        mock_execute.assert_awaited_once()
        args, kwargs = mock_execute.call_args
        assert kwargs["input_values"] == expected_input

    @pytest.mark.asyncio
    async def test_create_uses_merged_json(self, manager, mocker):
        """Test that `merge_set_values` is called when a JSON file is passed."""
        merge = mocker.patch(
            "gpp_client.mixins.create.merge_set_values",
            return_value={"merged": True},
        )
        mocker.patch.object(manager, "execute", return_value={"created": "ok"})
        mocker.patch.object(manager, "get_query", return_value="query { dummy }")

        await manager.create(set_values={"raw": True}, from_json_file=Path("fake.json"))

        merge.assert_called_once_with({"raw": True}, Path("fake.json"))
