from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def test_data_dir() -> Path:
    """Fixture that returns the path to the test data directory."""
    return Path(__file__).parent / "test_data"


@pytest.fixture
def gn_status_html(test_data_dir: Path) -> str:
    """Load the Gemini North status HTML file as a string."""
    return (test_data_dir / "gn_status.html").read_text(encoding="utf-8")


@pytest.fixture
def gmos_n_html(test_data_dir: Path) -> str:
    """Load the GMOS-N configuration HTML file as a string."""
    return (test_data_dir / "gmos_n.html").read_text(encoding="windows-1252")


@pytest.fixture
def gmos_s_html(test_data_dir: Path) -> str:
    """Load the GMOS-S configuration HTML file as a string."""
    return (test_data_dir / "gmos_s.html").read_text(encoding="windows-1252")


@pytest.fixture
def gs_json_payload(test_data_dir: Path) -> dict:
    """Load the Gemini South JSON payload as a dict."""
    import json

    return json.loads((test_data_dir / "gs_status.json").read_text(encoding="utf-8"))


class DummyClient:
    """Mock public-facing client exposing internal clients."""

    def __init__(self, internal, rest_client) -> None:
        self._client = internal
        self._rest_client = rest_client


@pytest.fixture
def internal(mocker):
    """
    Internal client with async query/mutation methods. This matches the minimal
    interface expected by all managers.
    """
    internal = mocker.MagicMock()
    internal.query = mocker.AsyncMock()
    internal.mutation = mocker.AsyncMock()
    return internal


@pytest.fixture
def rest_client(mocker):
    """Mock REST client wrapper."""
    rest_client = mocker.MagicMock()
    rest_client.get_session = mocker.AsyncMock()
    return rest_client


@pytest.fixture
def dummy_client(internal, rest_client) -> DummyClient:
    """Public-facing dummy client wrapper."""
    return DummyClient(internal, rest_client=rest_client)
