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
        NotAvailable
            If the selected environment does not serve the endpoint (404).
        GPPHttpError
            If GPP rejects the observation IDs (400) or answers another error
            status.
        GPPTransportError
            If GPP could not be reached, or the request timed out.
        """
        return await self._rest.get_atom_digests(
            observation_ids=observation_ids, accept_gzip=accept_gzip
        )
