import pytest
from pathlib import Path


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
