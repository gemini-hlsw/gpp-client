__all__ = ["SiteStatusManager"]

import re
from enum import Enum
from typing import Any, Literal, Optional

from httpx import AsyncClient
from bs4 import BeautifulSoup


class Site(str, Enum):
    SOUTH = "south"
    NORTH = "north"


SITE_CONFIG = {
    Site.NORTH: {
        "src_url": "https://www.gemini.edu/sciops/schedules/obsStatus/GN_Instrument.html",
        "gmos_url": "https://www.gemini.edu/sciops/schedules/obsStatus/gmosN.html",
        "shutter_keyword": "shutter",
        "instrument_keyword": "inst",
        "validity_keyword": "update",
    },
    Site.SOUTH: {
        "src_url": "https://www.gemini.edu/sciops/schedules/obsStatus/too_GS.json",
        "gmos_url": "https://www.gemini.edu/sciops/schedules/obsStatus/gmosS.html",
        "shutter_keyword": "open",
        "instrument_keyword": "instruments",
        "validity_keyword": "valid",
    },
}


class SiteStatusManager:
    async def get_by_id(self, site_id: Literal["south", "north"]) -> dict[str, Any]:
        """
        Get the current site status payload for Gemini North or South.

        Parameters
        ----------
        site_id : Literal["south", "north"]
            The observatory site name (case-insensitive).

        Returns
        -------
        dict[str, Any]
            A dictionary containing current status, instruments, and GMOS config info.
        """
        # Validate the site.
        site_key = site_id.strip().lower()
        site = Site(site_key)

        config = SITE_CONFIG[site]

        async with AsyncClient(follow_redirects=True) as client:
            if site == Site.NORTH:
                status_html = await self._fetch_webpage(client, config["src_url"])
                status_data = _parse_gemini_north_webpage(status_html)
                # Add site manually to match Gemini South payload.
                status_data["Site"] = "Gemini North"
            else:
                status_data = await self._fetch_json(client, config["src_url"])
            gmos_html = await self._fetch_webpage(client, config["gmos_url"])
            gmos_payload = _parse_gmos_config_page(gmos_html)

        shutter_payload = _parse_shutter(status_data.get(config["shutter_keyword"]))
        instruments_payload = _parse_instruments(
            status_data.get(config["instrument_keyword"])
        )

        return {
            "site": status_data.get("Site"),
            "validity": status_data.get(config["validity_keyword"]),
            "available": status_data.get("avail", ""),
            "instruments": instruments_payload,
            "comment": status_data.get("comment"),
            "shutter": shutter_payload,
            "gmos_config": gmos_payload,
        }

    async def _fetch_json(self, client: AsyncClient, url: str) -> dict[str, Any]:
        """
        Fetch JSON content from the given URL.

        Parameters
        ----------
        client : AsyncClient
            An HTTP client instance.
        url : str
            The URL to retrieve.

        Returns
        -------
        dict[str, Any]
            Parsed JSON content.
        """
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

    async def _fetch_webpage(self, client: AsyncClient, url: str) -> str:
        """
        Fetch a webpage.

        Parameters
        ----------
        client : AsyncClient
            An HTTP client instance.
        url : str
            The url to fetch.

        Returns
        -------
        str
            The returned html.
        """
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def _parse_gemini_north_webpage(html: str) -> dict[str, Any]:
    """
    Parse the Gemini North status HTML page to extract status values by ID.

    Parameters
    ----------
    html : str
        Raw HTML content from the Gemini North status page.

    Returns
    -------
    dict[str, Any]
        Dictionary of extracted values keyed by known element IDs.
    """
    soup = BeautifulSoup(html, "html.parser")

    ids_to_extract = [
        "update",
        "avail",
        "inst",
        "comment",
        "shutter",
    ]

    data: dict[str, Any] = {}
    for element_id in ids_to_extract:
        tag = soup.find(id=element_id)
        data[element_id] = tag.get_text(strip=True) if tag else None

    return data


def _parse_gmos_config_page(html: str) -> Optional[dict[str, Any]]:
    """
    Parse the GMOS configuration HTML page.

    Parameters
    ----------
    html : str
        Raw HTML content.

    Returns
    -------
    dict[str, Any], optional
        Contains timestamp, gratings, and slits.
    """
    if not html or not html.strip():
        return None

    soup = BeautifulSoup(html, "html.parser")
    h3_tags = soup.find_all("h3")

    # Extract timestamp from <h1>.
    timestamp = None
    h1 = soup.find("h1")
    if h1:
        parts = h1.get_text(strip=True).split(" at ")
        if len(parts) == 2:
            timestamp = parts[1].strip()

    # Expect first h3 = gratings, second h3 = slits.
    def collect_h5_between(start_tag, stop_tag=None) -> list[str]:
        h5_values = []
        for tag in start_tag.find_all_next("h5"):
            if stop_tag and tag == stop_tag:
                break
            h5_values.append(tag.get_text(strip=True))
        return h5_values

    gratings = []
    slits = []
    if len(h3_tags) >= 2:
        gratings = collect_h5_between(h3_tags[0], h3_tags[1])
        slits = collect_h5_between(h3_tags[1])

    return {
        "local_timestamp": timestamp,
        "gratings": gratings,
        "slits": slits,
    }


def _parse_shutter(raw: Optional[str]) -> Optional[dict[str, Any]]:
    """
    Parse the shutter status block.

    Parameters
    ----------
    raw : str, optional
        The raw shutter status string.

    Returns
    -------
    dict[str, Any], optional
        Parsed shutter state, timestamp (as string), and raw string.
    """
    if not raw or not raw.strip():
        return None

    # Strip any leading/trailing quotes and whitespace.
    raw_clean = raw.strip().replace('"', "")

    # Extract first word as state.
    state_match = re.match(r"(\w+)", raw_clean)
    state = state_match.group(1).lower() if state_match else None

    # Match ISO or slash-format datetime.
    timestamp_match = re.search(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}|\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}",
        raw,
    )

    return {
        "state": state,
        "timestamp": timestamp_match.group(0) if timestamp_match else None,
        "raw_string": raw,
    }


def _parse_instruments(raw: Optional[str]) -> Optional[dict[str, Any]]:
    """
    Parse the instruments block.

    Parameters
    ----------
    raw : str, optional
        The raw instruments string.

    Returns
    -------
    dict[str, Any], optional
        Parsed instruments list and raw string.
    """
    if not raw or not raw.strip():
        return None
    return {
        "available": raw.strip().split(),
        "raw_string": raw,
    }
