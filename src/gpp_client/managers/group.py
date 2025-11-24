__all__ = ["GroupManager"]

import logging
from pathlib import Path
from typing import Any, List, Optional

from gpp_client.api import (
    CreateGroupInput,
    Existence,
    GroupElementInput,
    GroupPropertiesInput,
    UpdateObservationsInput,
    WhereGroup,
    WhereOptionString,
    WhereOrderGroupId,
)
from gpp_client.api.custom_fields import (
    CreateGroupResultFields,
    GroupElementFields,
    GroupFields,
    ProgramFields,
    TimeSpanFields,
    UpdateGroupsResultFields,
)
from gpp_client.api.custom_mutations import Mutation
from gpp_client.api.custom_queries import Query
from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)


class GroupManager(BaseManager):
    GROUPS_RESULT_KEY = "groups"
    FIRST_INDEX = 0

    async def create(
        self,
        *,
        initial_contents: Optional[List[Optional[GroupElementInput]]] = None,
        properties: Optional[GroupPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a new group under a specified program.

        To pair it with a specific group of Observation see GroupElementInput.

        Parameters
        ----------
        initial_contents : List[Optional[GroupElementInput]], optional
            Allows the group to be populated with a list of GroupElementInputs.
        properties : GroupPropertiesInput, optional
            Group definition to be used in creation. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. It may be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        program_id : str, optional
            Direct program identifier. Must be provided if `proposal_reference` and
            `program_reference` are omitted.
        proposal_reference : str, optional
            Proposal label alternative to `program_id`.
        program_reference : str, optional
            Proposal label alternative to `program_id`.

        Returns
        -------
        dict[str, Any]
            The created group.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug(
            "Creating a new group under a program ID: %s, proposal reference: %s, or program reference: %s",
            program_id,
            proposal_reference,
            program_reference,
        )
        self.validate_single_identifier(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        )

        properties = self.load_properties(
            properties=properties, from_json=from_json, cls=GroupPropertiesInput
        )

        input_data = CreateGroupInput(
            program_id=program_id,
            program_reference=program_reference,
            set=properties,
            initial_contents=initial_contents,
        )

        fields = Mutation.create_group(input=input_data).fields(
            CreateGroupResultFields.group().fields(*self._fields())
        )
        operation_name = "createGroup"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def update_all(
        self,
        properties: GroupPropertiesInput,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereGroup] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update one or more groups with new properties.

        Parameters
        ----------
        properties : GroupPropertiesInput, optional
            Fields to update. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. It May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : Group, optional
            Filter expression to limit which observations are updated.
        limit : int, optional
            Maximum number of groups to update.
        include_deleted : bool, default=False
            Whether to include soft-deleted groups.

        Returns
        -------
        dict[str, Any]
            The update result and updated records.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug("Updating group(s)")
        properties = self.load_properties(
            properties=properties, from_json=from_json, cls=GroupPropertiesInput
        )

        input_data = UpdateObservationsInput(
            set=properties,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )
        fields = Mutation.update_groups(input=input_data).fields(
            UpdateGroupsResultFields.has_more,
            UpdateGroupsResultFields.groups().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )
        operation_name = "updateGroups"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def update_by_id(
        self,
        *,
        group_id: Optional[str] = None,
        group_name: Optional[str] = None,
        properties: GroupPropertiesInput,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update a single group with given ID.

        Parameters
        ----------
        group_id : str, optional
            Unique internal ID of the observation.
        group_name: str, optional
            Unique name of the group.
        properties : GroupPropertiesInput, optional
            Fields to update. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. It may be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted groups.
        include_deleted : bool, default=False
            Whether to include soft-deleted groups in the match.

        Returns
        -------
        dict[str, Any]
            The updated group.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``GPPValidationError``.
        """
        logger.debug("Updating group by ID: %s or name: %s", group_id, group_name)
        if group_id:
            where = WhereGroup(id=WhereOrderGroupId(eq=group_id))
        else:
            where = WhereGroup(name=WhereOptionString(eq=group_name))

        result = await self.update_all(
            where=where, limit=1, properties=properties, include_deleted=include_deleted
        )
        return result[GroupManager.GROUPS_RESULT_KEY][GroupManager.FIRST_INDEX]

    async def get_by_id(
        self,
        *,
        group_id: Optional[str] = None,
        group_name: Optional[str] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Get a single group with given ID.

        Parameters
        ----------
        group_id : str, optional
            Unique internal ID of the observation.
        group_name : str, optional
            Unique name of the group.
        include_deleted :bool, default=False
            Whether to include soft-deleted groups.

        Returns
        -------
        dict[str, Any]
            The retrieved group.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug("Getting group by ID: %s or name: %s", group_id, group_name)
        self.validate_single_identifier(
            group_id=group_id,
            group_name=group_name,
        )

        fields = Query.group(
            group_id=group_id,
            group_name=group_name,
        ).fields(*self._fields(include_deleted=include_deleted))

        operation_name = "group"
        result = await self.client.query(fields, operation_name=operation_name)
        return self.get_result(result, operation_name)

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereGroup | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        raise NotImplementedError("There is no groups query on the ODB")

    async def restore_by_id(
        self,
        group_id: Optional[str] = None,
        group_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Restore a soft-deleted group.

        Parameters
        ----------
        group_id : str, optional
            Unique internal ID of the group.
        group_name : str, optional
            Unique name of the group.

        Returns
        -------
        dict[str, Any]
            The restored group with `existence` set to PRESENT.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug("Restoring group by ID: %s or name: %s", group_id, group_name)
        properties = GroupPropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            group_id=group_id,
            group_name=group_name,
            properties=properties,
            include_deleted=True,
        )

    async def delete_by_id(
        self,
        *,
        group_id: Optional[str] = None,
        group_name: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Delete a soft-deleted group.

        Parameters
        ----------
        group_id: str, optional
            Unique internal ID of the group.
        group_name: str, optional
            Unique name of the group.

        Returns
        -------
        dict[str, Any]
            The deleted group with `existence` set to DELETED.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug("Deleting group by ID: %s or name: %s", group_id, group_name)
        properties = GroupPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            group_id=group_id,
            group_name=group_name,
            properties=properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool = False) -> tuple:
        return (
            GroupFields.id,
            GroupFields.parent_id,
            GroupFields.parent_index,
            GroupFields.program().fields(ProgramFields.id),
            GroupFields.name,
            GroupFields.description,
            GroupFields.minimum_required,
            GroupFields.minimum_interval().fields(TimeSpanFields.seconds),
            GroupFields.maximum_interval().fields(TimeSpanFields.seconds),
            GroupFields.ordered,
            GroupFields.elements(include_deleted=include_deleted).fields(
                GroupElementFields.parent_group_id,
                GroupElementFields.parent_index,
            ),
        )
