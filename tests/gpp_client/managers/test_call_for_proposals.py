import pytest
from polyfactory.factories.pydantic_factory import ModelFactory

from gpp_client.api.enums import Existence, Instrument
from gpp_client.api.input_types import CallForProposalsPropertiesInput
from gpp_client.managers.call_for_proposals import CallForProposalsManager


class CallForProposalsPropertiesInputFactory(
    ModelFactory[CallForProposalsPropertiesInput]
):
    """Factory for CallForProposalsPropertiesInput."""

    __model__ = CallForProposalsPropertiesInput
    __allow_none_optionals__ = False
    """Allow ``None`` for optional fields."""
    __use_defaults__ = False
    """Use default values for fields where applicable."""


class TestCallForProposalsCreate:
    """
    Test suite for CallForProposalsManager.
    """

    @pytest.fixture
    def mock_client(self, mocker):
        """
        Fixture that provides a mock client with mutation capability.
        """
        internal = mocker.MagicMock()
        internal.mutation = mocker.AsyncMock()

        class Wrapper:
            """
            Mock public-facing client that exposes _client internally.
            """

            _client = internal

        return Wrapper()

    @pytest.fixture
    def manager(self, mock_client) -> CallForProposalsManager:
        """
        Fixture that provides a CallForProposalsManager instance with a mock client.
        """
        return CallForProposalsManager(mock_client)

    @pytest.fixture
    def properties(self) -> CallForProposalsPropertiesInput:
        """s
        Fixture that provides a CallForProposalsPropertiesInput instance.
        """
        return CallForProposalsPropertiesInput(
            title="Test CFP",
            existence=Existence.PRESENT,
            semester="2025A",
            instruments=[Instrument.GMOS_NORTH],
        )

    @pytest.fixture
    def full_response(self) -> dict:
        """
        Fixture that provides a full response dictionary for createCallForProposals.
        """
        return {
            "id": "abc123",
            "title": "Test CFP",
            "type": "SCIENCE",
            "semester": "2025A",
            "active": {"start": "2025-01-01", "end": "2025-03-01"},
            "submissionDeadlineDefault": "2025-02-15",
            "instruments": ["GMOS-N", "GNIRS"],
            "existence": "PRESENT",
        }

    @pytest.mark.asyncio
    async def test_create_calls_get_result(
        self, manager, mock_client, mocker, properties, full_response
    ):
        """
        Ensure create() calls client.mutation and unpacks via get_result().
        """
        # Wrap the response in the expected GraphQL structure.
        operation_name = "createCallForProposals"
        wrapped_response = {operation_name: full_response}
        mock_client._client.mutation = mocker.AsyncMock(return_value=wrapped_response)

        # Spy get_result but do not mock it.
        spy = mocker.spy(manager, "get_result")

        result = await manager.create(properties=properties)

        # Ensure the unpack happened.
        spy.assert_called_once_with(
            wrapped_response,
            operation_name,
        )

        # Result should be unpacked.
        assert result == full_response, (
            "create() should return the unpacked inner payload from get_result(), "
            "but the returned value did not match the expected full_response."
        )
