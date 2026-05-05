__all__ = ["TargetDomain"]

import logging
from collections.abc import AsyncIterator

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.clone_target import CloneTarget
from gpp_client.generated.create_target_by_program_id import CreateTargetByProgramId
from gpp_client.generated.create_target_by_program_reference import (
    CreateTargetByProgramReference,
)
from gpp_client.generated.create_target_by_proposal_reference import (
    CreateTargetByProposalReference,
)
from gpp_client.generated.delete_target_by_id import DeleteTargetById
from gpp_client.generated.get_target_by_id import GetTargetById
from gpp_client.generated.get_targets import GetTargets
from gpp_client.generated.input_types import TargetPropertiesInput, WhereTarget
from gpp_client.generated.restore_target_by_id import RestoreTargetById
from gpp_client.generated.target_edit import TargetEdit
from gpp_client.generated.update_target_by_id import UpdateTargetById
from gpp_client.generated.update_targets import UpdateTargets

logger = logging.getLogger(__name__)


class TargetDomain(BaseDomain):
    async def clone(
        self,
        target_id: str,
        *,
        include_deleted: bool = False,
        properties: TargetPropertiesInput | None = None,
        replace_in: list[str] | None = None,
    ) -> CloneTarget:
        """
        Clone a target.

        Parameters
        ----------
        target_id : str
            The target ID to clone.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.
        properties : TargetPropertiesInput | None, optional
            Optional replacement properties for the cloned target.
        replace_in : list[str] | None, optional
            Optional observation IDs in which to replace the cloned target.

        Returns
        -------
        CloneTarget
            The generated GraphQL response model.
        """
        return await self._graphql.clone_target(
            target_id=target_id,
            include_deleted=include_deleted,
            properties=properties,
            replace_in=replace_in,
        )

    async def create_by_program_id(
        self,
        program_id: str,
        *,
        properties: TargetPropertiesInput,
        include_deleted: bool = False,
    ) -> CreateTargetByProgramId:
        """
        Create a target by program ID.

        Parameters
        ----------
        program_id : str
            The program ID.
        properties : TargetPropertiesInput
            The target properties.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.

        Returns
        -------
        CreateTargetByProgramId
            The generated GraphQL response model.
        """
        return await self._graphql.create_target_by_program_id(
            program_id=program_id,
            properties=properties,
            include_deleted=include_deleted,
        )

    async def create_by_program_reference(
        self,
        program_reference: str,
        *,
        properties: TargetPropertiesInput,
        include_deleted: bool = False,
    ) -> CreateTargetByProgramReference:
        """
        Create a target by program reference.

        Parameters
        ----------
        program_reference : str
            The program reference label.
        properties : TargetPropertiesInput
            The target properties.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.

        Returns
        -------
        CreateTargetByProgramReference
            The generated GraphQL response model.
        """
        return await self._graphql.create_target_by_program_reference(
            program_reference=program_reference,
            properties=properties,
            include_deleted=include_deleted,
        )

    async def create_by_proposal_reference(
        self,
        proposal_reference: str,
        *,
        properties: TargetPropertiesInput,
        include_deleted: bool = False,
    ) -> CreateTargetByProposalReference:
        """
        Create a target by proposal reference.

        Parameters
        ----------
        proposal_reference : str
            The proposal reference label.
        properties : TargetPropertiesInput
            The target properties.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.

        Returns
        -------
        CreateTargetByProposalReference
            The generated GraphQL response model.
        """
        return await self._graphql.create_target_by_proposal_reference(
            proposal_reference=proposal_reference,
            properties=properties,
            include_deleted=include_deleted,
        )

    async def update_all(
        self,
        *,
        properties: TargetPropertiesInput,
        include_deleted: bool = False,
        where: WhereTarget | None = None,
        limit: int | None = None,
    ) -> UpdateTargets:
        """
        Update targets in bulk.

        Parameters
        ----------
        properties : TargetPropertiesInput
            The properties to update.
        include_deleted : bool, default=False
            Whether deleted targets should be included in the update selection/result.
        where : WhereTarget | None, optional
            Optional target filter.
        limit : int | None, optional
            Optional update limit.

        Returns
        -------
        UpdateTargets
            The generated GraphQL response model.
        """
        return await self._graphql.update_targets(
            properties=properties,
            include_deleted=include_deleted,
            where=where,
            limit=limit,
        )

    async def update_by_id(
        self,
        target_id: str,
        *,
        properties: TargetPropertiesInput,
        include_deleted: bool = False,
    ) -> UpdateTargetById:
        """
        Update a target by ID.

        Parameters
        ----------
        target_id : str
            The target ID.
        properties : TargetPropertiesInput
            The properties to update.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.

        Returns
        -------
        UpdateTargetById
            The generated GraphQL response model.
        """
        return await self._graphql.update_target_by_id(
            target_id=target_id,
            properties=properties,
            include_deleted=include_deleted,
        )

    async def restore_by_id(
        self,
        target_id: str,
    ) -> RestoreTargetById:
        """
        Restore a target by ID.

        Parameters
        ----------
        target_id : str
            The target ID.

        Returns
        -------
        RestoreTargetById
            The generated GraphQL response model.
        """
        return await self._graphql.restore_target_by_id(target_id=target_id)

    async def delete_by_id(
        self,
        target_id: str,
    ) -> DeleteTargetById:
        """
        Delete a target by ID.

        Parameters
        ----------
        target_id : str
            The target ID.

        Returns
        -------
        DeleteTargetById
            The generated GraphQL response model.
        """
        return await self._graphql.delete_target_by_id(target_id=target_id)

    async def get_by_id(
        self,
        target_id: str,
        *,
        include_deleted: bool = False,
    ) -> GetTargetById:
        """
        Get a target by ID.

        Parameters
        ----------
        target_id : str
            The target ID.
        include_deleted : bool, default=False
            Whether deleted program data should be included in the result.

        Returns
        -------
        GetTargetById
            The generated GraphQL response model.
        """
        return await self._graphql.get_target_by_id(
            target_id=target_id,
            include_deleted=include_deleted,
        )

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereTarget | None = None,
        offset: str | None = None,
        limit: int | None = None,
    ) -> GetTargets:
        """
        Get targets matching the provided filters.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether deleted targets should be included.
        where : WhereTarget | None, optional
            Optional target filter.
        offset : str | None, optional
            Optional pagination offset.
        limit : int | None, optional
            Optional page size limit.

        Returns
        -------
        GetTargets
            The generated GraphQL response model.
        """
        return await self._graphql.get_targets(
            include_deleted=include_deleted,
            where=where,
            offset=offset,
            limit=limit,
        )

    async def subscribe_edits(
        self,
        *,
        target_id: str | None = None,
    ) -> AsyncIterator[TargetEdit]:
        """
        Subscribe to target edit events.

        Parameters
        ----------
        target_id : str | None, optional
            Restrict the subscription to a single target ID.

        Yields
        ------
        TargetEdit
            Target edit events.
        """
        async for event in self._graphql.target_edit(target_edit=target_id):
            yield event
