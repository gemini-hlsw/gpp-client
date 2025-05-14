__all__ = ['GroupManager']

from typing import Any, Optional

from pygments.lexer import include

from src.gpp_client.generated import CreateGroupInput, GroupPropertiesInput, WhereGroup, UpdateObservationsInput, \
    UpdateGroupsInput, WhereOrderGroupId, WhereOptionString, Existence
from src.gpp_client.generated.custom_fields import CreateGroupResultFields, UpdateGroupsResultFields, \
    UpdateObservationsResultFields, GroupFields, ProgramFields, GroupElementFields
from src.gpp_client.generated.custom_mutations import Mutation
from src.gpp_client.generated.custom_queries import Query
from src.gpp_client.managers.base_manager import BaseManager
from src.gpp_client.managers.utils import validate_single_identifier


class GroupManager(BaseManager):

    GROUPS_RESULT_KEY = 'groups'
    FIRST_INDEX = 0

    async def create(
            self,
            *,
            properties: GroupPropertiesInput,
            program_id: Optional[str] = None,
            program_reference: Optional[str] = None,
            include_deleted: bool = False,
    ) -> dict[str, Any]:

        validate_single_identifier()

        input_data = CreateGroupInput(
            program_id=program_id,
            program_reference=program_reference,
            set=properties,
            initialContents=None,
        )

        fields = Mutation.create_group(input=input_data).fields(
            CreateGroupResultFields.group().fields(*self._fields(include_deleted=include_deleted))
        )
        operation_name = "createGroup"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_all(
            self,
            properties: GroupPropertiesInput,
            where: Optional[WhereGroup] = None,
            limit: Optional[int] = None,
            include_deleted: bool = False,
    ) -> dict[str, Any]:

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
            )
        )
        operation_name = "updateGroups"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_by_id(
            self,
            *,
            group_id: Optional[str] = None,
            group_name: Optional[str] = None,
            properties: GroupPropertiesInput,
            include_deleted: bool = False,
    ) -> dict[str, Any]:

        if group_id:
            where = WhereGroup(id=WhereOrderGroupId(eq=group_id))
        else:
            where = WhereGroup(
                name=WhereOptionString(eq=group_name)
            )

        result = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            include_deleted=include_deleted
        )
        return result[GroupManager.GROUPS_RESULT_KEY][GroupManager.FIRST_INDEX]

    async def get_by_id(
            self,
            *,
            group_id: Optional[str] = None,
            group_name: Optional[str] = None,
            include_deleted: bool = False,
    ) -> dict[str, Any]:
        validate_single_identifier(
            group_id=group_id,
            group_name=group_name,
        )

        fields = Query.group(
            group_id=group_id,
            group_name=group_name,
        ).fields(*self._fields(include_deleted=include_deleted))

        operation_name = "group"
        result = await self.client.query(fields, operation_name=operation_name)
        return result[operation_name]

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
        properties = GroupPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            group_id=group_id,
            group_name=group_name,
            properties=properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool) -> tuple:
        return (
            GroupFields.id,
            GroupFields.parent_id,
            GroupFields.parent_index,
            GroupFields.program().fields(ProgramFields.id),
            GroupFields.name,
            GroupFields.description,
            GroupFields.minimum_required,
            GroupFields.ordered,
            GroupFields.elements(include_deleted=include_deleted).fields(
                GroupElementFields.parent_group_id,
                GroupElementFields.parent_index,
            ),
        )
