__all__ = ["ProgramManager"]

from pathlib import Path
from typing import Any, Optional

from ..api.custom_fields import (
    CreateProgramResultFields,
    DateIntervalFields,
    ProgramFields,
    ProgramSelectResultFields,
    ProgramUserFields,
    UpdateProgramsResultFields,
    GroupElementFields,
    GroupFields,
    ObservationFields,
    TimeSpanFields,
    ProposalFields,
    CallForProposalsFields,
)
from ..api.custom_mutations import Mutation
from ..api.custom_queries import Query
from ..api.enums import Existence
from ..api.input_types import (
    CreateProgramInput,
    ProgramPropertiesInput,
    UpdateProgramsInput,
    WhereOrderProgramId,
    WhereProgram,
)
from .base import BaseManager
from .utils import load_properties


class ProgramManager(BaseManager):
    async def create(
        self,
        *,
        properties: Optional[ProgramPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Create a new program.

        Parameters
        ----------
        properties : ProgramPropertiesInput, optional
            Full definition of the program to create. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.

        Returns
        -------
        dict[str, Any]
            The created program.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        properties = load_properties(
            properties=properties, from_json=from_json, cls=ProgramPropertiesInput
        )

        input_data = CreateProgramInput(
            set=properties,
        )

        fields = Mutation.create_program(input=input_data).fields(
            CreateProgramResultFields.program().fields(*self._fields()),
        )

        operation_name = "createProgram"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_all(
        self,
        *,
        properties: Optional[ProgramPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereProgram] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update multiple programs matching the given filter.

        Parameters
        ----------
        properties : ProgramPropertiesInput, optional
            Values to set on the matching programs. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : WhereProgram, optional
            Filter to determine which programs to update.
        limit : int, optional
            Maximum number of programs to update.
        include_deleted : bool, default=False
            Whether to include soft-deleted programs.

        Returns
        -------
        dict[str, Any]
            Update result and updated programs.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        properties = load_properties(
            properties=properties, from_json=from_json, cls=ProgramPropertiesInput
        )

        input_data = UpdateProgramsInput(
            set=properties,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )

        fields = Mutation.update_programs(input=input_data).fields(
            UpdateProgramsResultFields.has_more,
            UpdateProgramsResultFields.programs().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )

        operation_name = "updatePrograms"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_by_id(
        self,
        program_id: str,
        *,
        properties: Optional[ProgramPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update a single program by its ID.

        Parameters
        ----------
        program_id : str
            Unique identifier of the program to update.
        properties : ProgramPropertiesInput, optional
            New values to apply. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted programs in the update.

        Returns
        -------
        dict[str, Any]
            The updated program.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        where = WhereProgram(id=WhereOrderProgramId(eq=program_id))

        results = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            include_deleted=include_deleted,
            from_json=from_json,
        )

        # Since it returns one item, discard the 'matches' and return the item.
        return results["programs"][0]

    async def get_by_id(
        self, program_id: str, *, include_deleted: bool = False
    ) -> dict[str, Any]:
        """
        Fetch a single program by its ID.

        Parameters
        ----------
        program_id : str
            Unique identifier of the program.
        include_deleted : bool, default=False
            Whether to include deleted entries in the lookup.

        Returns
        -------
        dict[str, Any]
            Retrieved program.
        """
        fields = Query.program(program_id=program_id).fields(
            *self._fields(include_deleted=include_deleted)
        )

        operation_name = "program"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereProgram | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Fetch all programs with optional filters and pagination.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include deleted entries.
        where : WhereProgram, optional
            Optional filtering clause.
        offset : int, optional
            Pagination offset.
        limit : int, optional
            Maximum number of results.

        Returns
        -------
        dict[str, Any]
            Dictionary with `matches` and `hasMore`.
        """
        fields = Query.programs(
            include_deleted=include_deleted, where=where, offset=offset, limit=limit
        ).fields(
            ProgramSelectResultFields.has_more,
            ProgramSelectResultFields.matches().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )
        operation_name = "programs"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

    async def restore_by_id(self, program_id: str) -> dict[str, Any]:
        """
        Restore a soft-deleted program.

        Parameters
        ----------
        program_id : str
            Unique identifier of the program.

        Returns
        -------
        dict[str, Any]
            The restored program.
        """
        properties = ProgramPropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            program_id, properties=properties, include_deleted=True
        )

    async def delete_by_id(self, program_id: str) -> dict[str, Any]:
        """
        Soft-delete a program.

        Parameters
        ----------
        program_id : str
            Unique identifier of the program.

        Returns
        -------
        dict[str, Any]
            The deleted program payload.
        """
        properties = ProgramPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            program_id,
            properties=properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool = False) -> tuple:
        """
        Return the GraphQL fields to retrieve for a program.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include deleted resources when fetching related fields.

        Returns
        -------
        tuple
            GraphQL field structure.
        """
        return (
            ProgramFields.id,
            ProgramFields.name,
            ProgramFields.description,
            ProgramFields.existence,
            ProgramFields.type,
            ProgramFields.active().fields(
                DateIntervalFields.start, DateIntervalFields.end
            ),
            ProgramFields.proposal_status,
            ProgramFields.proposal().fields(
                ProposalFields.call().fields(
                    CallForProposalsFields.semester,
                    CallForProposalsFields.active().fields(
                        DateIntervalFields.start, DateIntervalFields.end
                    ),
                ),
                ProposalFields.type(),
            ),
            ProgramFields.pi().fields(
                ProgramUserFields.id,
            ),
            ProgramFields.all_group_elements(include_deleted).fields(
                GroupElementFields.parent_group_id,
                GroupElementFields.observation().fields(
                    ObservationFields.id, ObservationFields.group_id
                ),
                GroupElementFields.group().fields(
                    GroupFields.id,
                    GroupFields.name,
                    GroupFields.minimum_required,
                    GroupFields.ordered,
                    GroupFields.parent_id,
                    GroupFields.parent_index,
                    GroupFields.minimum_interval().fields(TimeSpanFields.seconds),
                    GroupFields.maximum_interval().fields(TimeSpanFields.seconds),
                ),
            ),
        )
