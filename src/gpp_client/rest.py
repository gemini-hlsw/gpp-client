"""
REST API client for non-GraphQL requests.
"""

__all__ = ["_GPPRESTClient"]

import asyncio
import gzip
import logging
import ssl
from urllib.parse import urlparse

import aiohttp
import certifi

logger = logging.getLogger(__name__)


class _GPPRESTClient:
    """
    REST API client to non-GraphQL requests that help with the function of managers and
    coordinators.

    Attributes
    ----------
    base_url : str
        Base URL of the REST API. Derived from GPPClient base_url.
    gpp_token : str
        GPP token to authenticate against the REST API. Same as GPPClient.
    timeout : float
        Timeout for REST API requests in seconds.
    """

    _DEFAULT_TIMEOUT = 30.0  # Seconds.

    def __init__(
        self, resolved_url: str, gpp_token: str, timeout: float = _DEFAULT_TIMEOUT
    ) -> None:
        self.base_url = self.get_base_url(resolved_url)
        self.gpp_token = gpp_token
        self._timeout = timeout

        self._session: aiohttp.ClientSession | None = None
        self._lock = asyncio.Lock()

    def resolve_headers(self) -> dict[str, str]:
        """
        Resolve the headers for the REST API requests.

        Returns
        -------
        dict[str, str]
            Headers dictionary.
        """
        headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {self.gpp_token}",
        }
        return headers

    async def get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an ``aiohttp.ClientSession`` for making REST API requests.

        Returns
        -------
        aiohttp.ClientSession
            The aiohttp ClientSession instance.
        """
        async with self._lock:
            if self._session is None or self._session.closed:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                connector = aiohttp.TCPConnector(ssl=ssl_context)
                self._session = aiohttp.ClientSession(
                    base_url=self.base_url,
                    timeout=aiohttp.ClientTimeout(total=self._timeout),
                    connector=connector,
                    headers=self.resolve_headers(),
                )
            return self._session

    async def close(self) -> None:
        """
        Close the session if it exists and is not already closed.
        """
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def get_base_url(self, url: str) -> str:
        """
        Get the base URL from a full URL.

        Parameters
        ----------
        url : str
            Full URL string.

        Returns
        -------
        str
            Base URL string.
        """
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    async def get_atom_digests(
        self, observation_ids: list, accept_gzip: bool = True
    ) -> str:
        """
        Request atom digests for the given observation IDs.

        Parameters
        ----------
        observation_ids : list
             List of observation ID strings.
        accept_gzip : bool
            Whether to accept gzip compression.

        Returns
        -------
        str
            TSV data as string.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP errors.
        ValueError
            For invalid observation IDs.
        """
        headers = self.resolve_headers()
        if accept_gzip:
            headers["Accept-Encoding"] = "gzip"

        # Prepare body - one observation ID per line
        body = "\n".join(observation_ids)

        session = await self.get_session()

        async with session.post(
            "/scheduler/atoms", data=body, headers=headers
        ) as response:
            # Handle different response codes
            if response.status == 400:
                error_text = await response.text()
                raise ValueError(f"Invalid observation IDs: {error_text}")
            elif response.status == 403:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Access forbidden - check authentication and permissions",
                )
            elif response.status != 200:
                response.raise_for_status()

            # Handle gzipped response
            content_encoding = response.headers.get("Content-Encoding", "").lower()
            if content_encoding == "gzip":
                try:
                    content = await response.read()
                    return gzip.decompress(content).decode("utf-8")
                except gzip.BadGzipFile:
                    # Server claimed gzip but sent plain text
                    return await response.text()
            else:
                return await response.text()
