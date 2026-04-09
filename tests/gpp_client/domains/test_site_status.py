"""Tests for the site status domain."""

from __future__ import annotations

import pytest

from gpp_client.domains.site_status import (
    SITE_CONFIG,
    Site,
    SiteStatusDomain,
    _parse_gemini_north_webpage,
    _parse_gmos_config_page,
    _parse_instruments,
    _parse_shutter,
)


def test_parse_gemini_north_webpage_extracts_known_ids() -> None:
    """
    Ensure Gemini North HTML parsing extracts known element ids.
    """
    html = """
    <html>
        <div id="update">2025-01-01</div>
        <div id="avail">Available</div>
        <div id="inst">GMOS GNIRS</div>
        <div id="comment">All good</div>
        <div id="shutter">Open 2025-01-01T12:00:00</div>
    </html>
    """

    result = _parse_gemini_north_webpage(html)

    assert result == {
        "update": "2025-01-01",
        "avail": "Available",
        "inst": "GMOS GNIRS",
        "comment": "All good",
        "shutter": "Open 2025-01-01T12:00:00",
    }


def test_parse_gmos_config_page_returns_none_for_empty_html() -> None:
    """
    Ensure GMOS config parser returns None for empty html.
    """
    assert _parse_gmos_config_page("") is None


def test_parse_gmos_config_page_extracts_timestamp_gratings_and_slits() -> None:
    """
    Ensure GMOS config parser extracts timestamp gratings and slits.
    """
    html = """
    <html>
        <h1>GMOS Config at 2025-01-01 12:00</h1>
        <h3>Gratings</h3>
        <h5>B600</h5>
        <h5>R400</h5>
        <h3>Slits</h3>
        <h5>0.5 arcsec</h5>
        <h5>1.0 arcsec</h5>
    </html>
    """

    result = _parse_gmos_config_page(html)

    assert result == {
        "local_timestamp": "2025-01-01 12:00",
        "gratings": ["B600", "R400"],
        "slits": ["0.5 arcsec", "1.0 arcsec"],
    }


def test_parse_shutter_returns_none_for_empty_input() -> None:
    """
    Ensure shutter parser returns None for empty input.
    """
    assert _parse_shutter(None) is None
    assert _parse_shutter("   ") is None


def test_parse_shutter_extracts_state_and_timestamp() -> None:
    """
    Ensure shutter parser extracts state timestamp and raw string.
    """
    raw = "Open 2025-01-01T12:34:56"
    result = _parse_shutter(raw)

    assert result == {
        "state": "open",
        "timestamp": "2025-01-01T12:34:56",
        "raw_string": raw,
    }


def test_parse_instruments_returns_none_for_empty_input() -> None:
    """
    Ensure instruments parser returns None for empty input.
    """
    assert _parse_instruments(None) is None
    assert _parse_instruments("  ") is None


def test_parse_instruments_splits_available_instruments() -> None:
    """
    Ensure instruments parser splits whitespace-separated values.
    """
    raw = "GMOS GNIRS GPI"

    result = _parse_instruments(raw)

    assert result == {
        "available": ["GMOS", "GNIRS", "GPI"],
        "raw_string": raw,
    }


@pytest.mark.asyncio
async def test_fetch_json_returns_parsed_payload(mocker) -> None:
    """
    Ensure _fetch_json returns parsed json content.
    """
    domain = SiteStatusDomain()
    response = mocker.Mock()
    response.json.return_value = {"ok": True}
    response.raise_for_status = mocker.Mock()
    client = mocker.Mock()
    client.get = mocker.AsyncMock(return_value=response)

    result = await domain._fetch_json(client, "https://example.test")

    assert result == {"ok": True}
    client.get.assert_awaited_once_with("https://example.test")
    response.raise_for_status.assert_called_once_with()


@pytest.mark.asyncio
async def test_fetch_webpage_returns_text(mocker) -> None:
    """
    Ensure _fetch_webpage returns response text.
    """
    domain = SiteStatusDomain()
    response = mocker.Mock()
    response.text = "<html></html>"
    response.raise_for_status = mocker.Mock()
    client = mocker.Mock()
    client.get = mocker.AsyncMock(return_value=response)

    result = await domain._fetch_webpage(client, "https://example.test")

    assert result == "<html></html>"
    client.get.assert_awaited_once_with("https://example.test")
    response.raise_for_status.assert_called_once_with()


@pytest.mark.asyncio
async def test_get_by_id_for_north_builds_expected_payload(mocker) -> None:
    """
    Ensure get_by_id for north builds the expected payload.
    """
    domain = SiteStatusDomain()

    mocker.patch.object(
        domain,
        "_fetch_webpage",
        side_effect=[
            """
            <html>
                <div id="update">2025-01-01</div>
                <div id="avail">Available</div>
                <div id="inst">GMOS GNIRS</div>
                <div id="comment">All good</div>
                <div id="shutter">Open 2025-01-01T12:00:00</div>
            </html>
            """,
            """
            <html>
                <h1>GMOS Config at 2025-01-01 12:00</h1>
                <h3>Gratings</h3>
                <h5>B600</h5>
                <h3>Slits</h3>
                <h5>0.5 arcsec</h5>
            </html>
            """,
        ],
    )

    result = await domain.get_by_id("north")

    assert result["site"] == "Gemini North"
    assert result["validity"] == "2025-01-01"
    assert result["available"] == "Available"
    assert result["comment"] == "All good"
    assert result["instruments"]["available"] == ["GMOS", "GNIRS"]
    assert result["shutter"]["state"] == "open"
    assert result["gmos_config"]["gratings"] == ["B600"]


@pytest.mark.asyncio
async def test_get_by_id_for_south_builds_expected_payload(mocker) -> None:
    """
    Ensure get_by_id for south builds the expected payload.
    """
    domain = SiteStatusDomain()

    mocker.patch.object(
        domain,
        "_fetch_json",
        return_value={
            "Site": "Gemini South",
            "valid": "2025-01-01",
            "avail": "Available",
            "comment": "All good",
            "open": "Open 2025/01/01 12:00:00",
            "instruments": "GMOS Flamingos",
        },
    )
    mocker.patch.object(
        domain,
        "_fetch_webpage",
        return_value="""
        <html>
            <h1>GMOS Config at 2025-01-01 12:00</h1>
            <h3>Gratings</h3>
            <h5>B600</h5>
            <h3>Slits</h3>
            <h5>0.5 arcsec</h5>
        </html>
        """,
    )

    result = await domain.get_by_id("south")

    assert result["site"] == "Gemini South"
    assert result["validity"] == "2025-01-01"
    assert result["available"] == "Available"
    assert result["comment"] == "All good"
    assert result["instruments"]["available"] == ["GMOS", "Flamingos"]
    assert result["shutter"]["state"] == "open"
    assert result["gmos_config"]["slits"] == ["0.5 arcsec"]


def test_site_config_contains_expected_sites() -> None:
    """
    Ensure site config contains both supported sites.
    """
    assert set(SITE_CONFIG.keys()) == {Site.NORTH, Site.SOUTH}
