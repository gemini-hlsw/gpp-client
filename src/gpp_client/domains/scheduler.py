__all__ = ["SchedulerDomain"]

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.get_scheduler_all_programs_id import (
    GetSchedulerAllProgramsId,
)
from gpp_client.generated.get_scheduler_programs import GetSchedulerPrograms


class SchedulerDomain(BaseDomain):
    async def get_programs(
        self,
        *,
        programs_list: list[str] | None = None,
    ) -> GetSchedulerPrograms:
        """
        Get scheduler programs.

        Parameters
        ----------
        programs_list : list[str] | None, optional
            Optional list of program IDs to restrict the result set.

        Returns
        -------
        GetSchedulerPrograms
            The generated GraphQL response model.
        """
        return await self._graphql.get_scheduler_programs(programs_list=programs_list)

    async def get_program_ids(
        self,
    ) -> GetSchedulerAllProgramsId:
        """
        Get all scheduler program IDs.

        Returns
        -------
        GetSchedulerAllProgramsId
            The generated GraphQL response model.
        """
        return await self._graphql.get_scheduler_all_programs_id()
