import aiohttp
import asyncio
import certifi
import gzip
import ssl


__all__ = ["_GPPRESTClient"]


class _GPPRESTClient:
    """
    REST API client to non-GraphQL requests that help with the function of managers and coordinators.

    Attributes
    ----------
    base_url : str
        Base URL of the REST API. Derived from GPPClient base_url.
    gpp_token : str
        GPP token to authenticate against the REST API. Same as GPPClient.
    """

    def __init__(self, resolved_url: str, gpp_token: str) -> None:
        self.base_url = resolved_url.rstrip("/odb")
        self.gpp_token = gpp_token
        self._session = None
        self._lock = asyncio.Lock()

    def resolve_headers(self):
        headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Bearer {self.gpp_token}",
        }
        return headers

    async def _get_session(self):
        async with self._lock:
            if self._session is None or self._session.closed:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                connector = aiohttp.TCPConnector(ssl=ssl_context)
                headers = self.resolve_headers()
                self._session = aiohttp.ClientSession(
                    base_url=self.base_url,
                    timeout=aiohttp.ClientTimeout(total=30),
                    connector=connector,
                    headers=headers,
                )
            return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

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

        session = await self._get_session()

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
