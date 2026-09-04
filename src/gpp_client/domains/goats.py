"""
Module for GOATS-related operations.
"""

__all__ = ["GOATSDomain"]

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.get_goats_config_options import GetGOATSConfigOptions
from gpp_client.generated.get_goats_configuration_requests import (
    GetGOATSConfigurationRequests,
)
from gpp_client.generated.get_goats_observations import GetGOATSObservations
from gpp_client.generated.get_goats_programs import GetGOATSPrograms


class GOATSDomain(BaseDomain):
    """
    Domain class for GOATS-related operations.
    """

    async def get_observations_by_program_id(
        self,
        *,
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

    async def get_configuration_requests_by_program_id(
        self,
        *,
        program_id: str,
    ) -> GetGOATSConfigurationRequests:
        """
        Get the approved GOATS configuration requests for a program.

        Parameters
        ----------
        program_id : str
            The program ID.

        Returns
        -------
        GetGOATSConfigurationRequests
            The generated GraphQL response model.
        """
        return await self._graphql.get_goats_configuration_requests(
            program_id=program_id
        )

    async def get_config_options(
        self,
        *,
        instrument: str,
    ) -> GetGOATSConfigOptions:
        """
        Get the valid spectroscopy and imaging configuration options.

        Parameters
        ----------
        instrument : str
            The instrument to get the options for.

        Returns
        -------
        GetGOATSConfigOptions
            The generated GraphQL response model.
        """
        return await self._graphql.get_goats_config_options(instrument=instrument)
