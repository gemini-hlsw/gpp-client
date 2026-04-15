"""
Module for atom-related operations.
"""

__all__ = ["AtomDomain"]

import logging

from gpp_client.domains.base import BaseDomain

logger = logging.getLogger(__name__)


class AtomDomain(BaseDomain):
    """
    Domain for interacting with atom-related API endpoints.
    """

    async def get_digests(
        self, *, observation_ids: list[str], accept_gzip: bool = True
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
        return await self._rest._get_atom_digest(
            observation_ids=observation_ids, accept_gzip=accept_gzip
        )
