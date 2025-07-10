__all__ = ["ObservationCoordinator"]

from typing import Any

from ....coordinator import BaseCoordinator


class ObservationCoordinator(BaseCoordinator):
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
        results = await self.client._client.get_goats_observations(
            program_id=program_id
        )
        return results.model_dump()
