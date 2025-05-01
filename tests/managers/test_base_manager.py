import pytest

from gpp_client.managers.base_manager import BaseManager


class DummyClient:
    async def _execute(self, query, variables=None):
        return {"data": "mocked", "query": query, "variables": variables}


class DummyManager(BaseManager):
    default_fields = "id name"
    resource_id_field = "testId"
    queries = {
        "get_by_id": "query GetById { resource { {fields} } }",
        "create": "mutation CreateResource { create(input: {fields}) }",
    }


@pytest.fixture
def manager():
    """Return a DummyManager instance for testing."""
    return DummyManager(client=DummyClient())


class TestBaseManager:
    def test_registered_queries(self, manager):
        """Test that registered_queries returns non-None query keys."""
        assert manager.registered_queries == {"get_by_id", "create"}

    def test_get_query_valid(self, manager):
        """Test that get_query uses default_fields when none are provided."""
        query = manager.get_query(query_id="get_by_id")
        assert "id name" in query

    def test_get_query_custom_fields(self, manager):
        """Test that get_query uses custom fields if provided."""
        query = manager.get_query(query_id="create", fields="title text")
        assert "title text" in query

    def test_get_query_invalid(self, manager):
        """Test that requesting an undefined query ID raises a ValueError."""
        with pytest.raises(ValueError):
            manager.get_query(query_id="unknown")

    def test_get_default_fields(self, manager):
        """Test that get_default_fields returns the correct default."""
        assert manager.get_default_fields() == "id name"

    def test_get_resource_id_field(self, manager):
        """Test that get_resource_id_field returns the correct ID field."""
        assert manager.get_resource_id_field() == "testId"

    def test_submanager_registration(self, manager):
        """Test registering and accessing a submanager."""
        sub = DummyManager(client=DummyClient())
        manager.register_submanager("child", sub)
        assert manager.get_submanager("child") == sub
        assert hasattr(manager, "child")

    @pytest.mark.asyncio
    async def test_execute_with_input_and_selector(self, mocker, manager):
        """Test that execute delegates properly to the client's _execute method."""
        mock_execute = mocker.patch.object(
            manager._client, "_execute", return_value={"mock": "ok"}
        )

        query = "mutation UpdateResource { ... }"
        input_values = {"SET": {"name": "New"}}
        selector_values = {"limit": 1}

        result = await manager.execute(
            query=query, input_values=input_values, selector_values=selector_values
        )

        assert result == {"mock": "ok"}
        mock_execute.assert_awaited_once_with(
            query=query, variables={"input": input_values, "limit": 1}
        )
