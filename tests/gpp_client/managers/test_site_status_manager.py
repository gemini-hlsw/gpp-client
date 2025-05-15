import pytest
from gpp_client.managers.site_status import (
    _parse_gemini_north_webpage,
    _parse_gmos_config_page,
    _parse_shutter,
    _parse_instruments,
    SiteStatusManager,
)


@pytest.mark.asyncio
async def test_invalid_site_id_raises():
    manager = SiteStatusManager()
    with pytest.raises(ValueError):
        await manager.get_by_id("invalid")


def test__parse_gemini_north_webpage(gn_status_html):
    result = _parse_gemini_north_webpage(gn_status_html)
    assert isinstance(result, dict)
    assert "update" in result
    assert "shutter" in result
    assert result["update"].startswith("Valid until")
    assert result["shutter"] is not None


@pytest.mark.parametrize("fixture_name", ["gmos_n_html", "gmos_s_html"])
def test__parse_gmos_config_page(request, fixture_name):
    html = request.getfixturevalue(fixture_name)
    result = _parse_gmos_config_page(html)
    assert isinstance(result, dict)
    assert "gratings" in result
    assert "slits" in result
    assert isinstance(result["gratings"], list)
    assert isinstance(result["slits"], list)
    assert "local_timestamp" in result
    assert isinstance(result["local_timestamp"], str)


def test__parse_shutter_valid():
    raw = "OPEN (as of 2025/05/15 17:55:02)."
    result = _parse_shutter(raw)
    assert result["state"] == "open"
    assert result["timestamp"] == "2025/05/15 17:55:02"
    assert result["raw_string"] == raw


def test__parse_shutter_iso():
    raw = '"CLOSED (as of 2025-05-15T10:45:01).'
    result = _parse_shutter(raw)
    assert result["state"] == "closed"
    assert result["timestamp"] == "2025-05-15T10:45:01"


def test__parse_instruments_valid():
    raw = "GMOS-N GNIRS FLAMINGOS-2"
    result = _parse_instruments(raw)
    assert result["available"] == ["GMOS-N", "GNIRS", "FLAMINGOS-2"]
    assert result["raw_string"] == raw


def test__parse_instruments_none():
    assert _parse_instruments(None) is None
    assert _parse_instruments("") is None


def test__parse_shutter_from_json(gs_json_payload):
    raw = gs_json_payload.get("open")
    result = _parse_shutter(raw)

    assert isinstance(result, dict)
    assert "state" in result
    assert "timestamp" in result
    assert result["raw_string"] == raw


def test__parse_instruments_from_json(gs_json_payload):
    raw = gs_json_payload.get("instruments")
    result = _parse_instruments(raw)

    assert isinstance(result, dict)
    assert "available" in result
    assert isinstance(result["available"], list)
    assert result["raw_string"] == raw
