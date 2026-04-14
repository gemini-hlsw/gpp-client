"""
Module for retrieving and managing program information.
"""

__all__ = ["ProgramDomain"]

import logging
from collections.abc import AsyncIterator

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.create_program import CreateProgram
from gpp_client.generated.delete_program_by_id import DeleteProgramById
from gpp_client.generated.get_program_by_id import GetProgramById
from gpp_client.generated.get_program_by_proposal_reference import (
    GetProgramByProposalReference,
)
from gpp_client.generated.get_program_by_reference import GetProgramByReference
from gpp_client.generated.get_programs import GetPrograms
from gpp_client.generated.input_types import ProgramPropertiesInput, WhereProgram
from gpp_client.generated.program_edit import ProgramEdit
from gpp_client.generated.restore_program_by_id import RestoreProgramById
from gpp_client.generated.update_program_by_id import UpdateProgramById
from gpp_client.generated.update_programs import UpdatePrograms

logger = logging.getLogger(__name__)


class ProgramDomain(BaseDomain):
    """
    Domain for retrieving and managing program information.
    """

    async def create(
        self,
        *,
        include_deleted: bool = False,
        properties: ProgramPropertiesInput | None = None,
    ) -> CreateProgram:
        """
        Create a program.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether related deleted records should be included in the response.
        properties : ProgramPropertiesInput | None, optional
            The program properties to create.

        Returns
        -------
        CreateProgram
            The generated GraphQL response model.
        """
        return await self._graphql.create_program(
            include_deleted=include_deleted,
            properties=properties,
        )

    async def update_all(
        self,
        *,
        properties: ProgramPropertiesInput,
        include_deleted: bool = False,
        where: WhereProgram | None = None,
        limit: int | None = None,
    ) -> UpdatePrograms:
        """
        Update programs using a bulk update.

        Parameters
        ----------
        properties : ProgramPropertiesInput
            The properties to update.
        include_deleted : bool, default=False
            Whether deleted programs should be included in matching/updating.
        where : WhereProgram | None, optional
            Optional filter for matching programs.
        limit : int | None, optional
            Optional maximum number of programs to update.

        Returns
        -------
        UpdatePrograms
            The generated GraphQL response model.
        """
        return await self._graphql.update_programs(
            properties=properties,
            include_deleted=include_deleted,
            where=where,
            limit=limit,
        )

    async def update_by_id(
        self,
        program_id: str,
        *,
        properties: ProgramPropertiesInput,
        include_deleted: bool = False,
    ) -> UpdateProgramById:
        """
        Update a program by ID.

        Parameters
        ----------
        program_id : str
            The program ID.
        properties : ProgramPropertiesInput
            The properties to update.
        include_deleted : bool, default=False
            Whether deleted programs should be included.

        Returns
        -------
        UpdateProgramById
            The generated GraphQL response model.
        """
        return await self._graphql.update_program_by_id(
            program_id=program_id,
            properties=properties,
            include_deleted=include_deleted,
        )

    async def restore_by_id(
        self,
        program_id: str,
    ) -> RestoreProgramById:
        """
        Restore a program by ID.

        Parameters
        ----------
        program_id : str
            The program ID.

        Returns
        -------
        RestoreProgramById
            The generated GraphQL response model.
        """
        return await self._graphql.restore_program_by_id(program_id=program_id)

    async def delete_by_id(
        self,
        program_id: str,
    ) -> DeleteProgramById:
        """
        Delete a program by ID.

        Parameters
        ----------
        program_id : str
            The program ID.

        Returns
        -------
        DeleteProgramById
            The generated GraphQL response model.
        """
        return await self._graphql.delete_program_by_id(program_id=program_id)

    async def get_by_id(
        self,
        program_id: str,
        *,
        include_deleted: bool = False,
    ) -> GetProgramById:
        """
        Get a program by ID.

        Parameters
        ----------
        program_id : str
            The program ID.
        include_deleted : bool, default=False
            Whether deleted related records should be included.

        Returns
        -------
        GetProgramById
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_by_id(
            program_id=program_id,
            include_deleted=include_deleted,
        )

    async def get_by_reference(
        self,
        program_reference: str,
        *,
        include_deleted: bool = False,
    ) -> GetProgramByReference:
        """
        Get a program by program reference.

        Parameters
        ----------
        program_reference : str
            The program reference label.
        include_deleted : bool, default=False
            Whether deleted related records should be included.

        Returns
        -------
        GetProgramByReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_by_reference(
            program_reference=program_reference,
            include_deleted=include_deleted,
        )

    async def get_by_proposal_reference(
        self,
        proposal_reference: str,
        *,
        include_deleted: bool = False,
    ) -> GetProgramByProposalReference:
        """
        Get a program by proposal reference.

        Parameters
        ----------
        proposal_reference : str
            The proposal reference label.
        include_deleted : bool, default=False
            Whether deleted related records should be included.

        Returns
        -------
        GetProgramByProposalReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_by_proposal_reference(
            proposal_reference=proposal_reference,
            include_deleted=include_deleted,
        )

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereProgram | None = None,
        offset: str | None = None,
        limit: int | None = None,
    ) -> GetPrograms:
        """
        Get programs matching the provided filters.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether deleted programs should be included.
        where : WhereProgram | None, optional
            Optional program filter.
        offset : str | None, optional
            Optional pagination offset.
        limit : int | None, optional
            Optional page size limit.

        Returns
        -------
        GetPrograms
            The generated GraphQL response model.
        """
        return await self._graphql.get_programs(
            include_deleted=include_deleted,
            where=where,
            offset=offset,
            limit=limit,
        )

    async def subscribe_to_edits(
        self,
        *,
        program_id: str | None = None,
    ) -> AsyncIterator[ProgramEdit]:
        """
        Subscribe to program edit events.

        Parameters
        ----------
        program_id : str | None, optional
            Restrict the subscription to a single program ID.

        Yields
        ------
        ProgramEdit
            Program edit events.
        """
        async for event in self._graphql.program_edit(program_id=program_id):
            yield event
