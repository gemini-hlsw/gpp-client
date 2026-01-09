__all__ = ["GOATSObservationCoordinator"]

import logging
from typing import Any

from gpp_client.coordinator import BaseCoordinator
from gpp_client.exceptions import GPPClientError

logger = logging.getLogger(__name__)


class GOATSObservationCoordinator(BaseCoordinator):
    """
    Modifies the return of the observation manager to return the GOATS payload.
    """

    async def get_all(self, *, program_id: str) -> dict[str, Any]:
        """
        Retrieve the GOATS-specific observations for a program ID.

        Parameters
        ----------
        program_id : str
            The ID for the observing program.

        Returns
        -------
        dict[str, Any]
            The GOATS-specific observations payload.
        """
        logger.debug("Retrieving GOATS observations for program ID: %s", program_id)
        results = await self.client._client.get_goats_observations(
            program_id=program_id
        )
        try:
            return results.model_dump(by_alias=True)["observations"]
        except KeyError as exc:
            message = (
                "Unexpected response structure when retrieving GOATS "
                f"observations: {exc}"
            )
            logger.error(message, exc_info=False)
            raise GPPClientError(message) from None
