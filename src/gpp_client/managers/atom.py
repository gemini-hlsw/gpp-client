__all__ = ["AttachmentManager"]

import gzip
import logging

import aiohttp

from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)


class AttachmentManager(BaseManager):
    async def get_atom_digests(
        self, observation_ids: list[str], accept_gzip: bool = True
    ) -> str:
        """
        Request atom digests for the given observation IDs.

        Parameters
        ----------
        observation_ids : list[str]
             List of observation ID strings.
        accept_gzip : bool, default=True
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
        headers = {}
        if accept_gzip:
            headers["Accept-Encoding"] = "gzip"

        # Prepare body - one observation ID per line.
        body = "\n".join(observation_ids)

        session = await self.rest_client._get_session()

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
                    # Server claimed gzip but sent plain text.
                    return await response.text()
            else:
                return await response.text()
