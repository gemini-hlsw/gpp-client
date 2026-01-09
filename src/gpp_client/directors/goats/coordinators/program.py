__all__ = ["GOATSProgramCoordinator"]

from typing import Any

from ....coordinator import BaseCoordinator


class GOATSProgramCoordinator(BaseCoordinator):
    """
    Modifies the return of the program manager to return the GOATS payload.
    """

    async def get_all(self) -> dict[str, Any]:
        """
        Retrieve all programs with accepted proposals.

        Returns
        -------
        dict[str, Any]
            The GOATS-specific programs payload.
        """
        results = await self.client._client.get_goats_programs()
        return results.model_dump(by_alias=True)["programs"]
