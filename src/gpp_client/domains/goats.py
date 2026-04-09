__all__ = ["GOATSDomain"]

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.get_goats_observations import GetGOATSObservations
from gpp_client.generated.get_goats_programs import GetGOATSPrograms


class GOATSDomain(BaseDomain):
    async def get_observations_by_program_id(
        self,
        program_id: str,
    ) -> GetGOATSObservations:
        """
        Get GOATS observations for a program.

        Parameters
        ----------
        program_id : str
            The program ID.

        Returns
        -------
        GetGOATSObservations
            The generated GraphQL response model.
        """
        return await self._graphql.get_goats_observations(program_id=program_id)

    async def get_programs(self) -> GetGOATSPrograms:
        """
        Get GOATS programs.

        Returns
        -------
        GetGOATSPrograms
            The generated GraphQL response model.
        """
        return await self._graphql.get_goats_programs()
