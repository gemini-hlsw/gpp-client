__all__ = ["TargetManager"]

from pathlib import Path
from typing import Any, Optional

from ..api.custom_fields import (
    CreateTargetResultFields,
    ProgramFields,
    TargetFields,
    TargetSelectResultFields,
    UpdateTargetsResultFields,
)
from ..api.custom_mutations import Mutation
from ..api.custom_queries import Query
from ..api.enums import Existence
from ..api.input_types import (
    CreateTargetInput,
    TargetPropertiesInput,
    UpdateTargetsInput,
    WhereOrderTargetId,
    WhereTarget,
)
from .base import BaseManager
from .utils import load_properties, validate_single_identifier


class TargetManager(BaseManager):
    async def create(
        self,
        *,
        properties: Optional[TargetPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a new target using a fully defined ``TargetPropertiesInput``.

        Parameters
        ----------
        properties : TargetPropertiesInput, optional
            Full target definition. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        program_id : str, optional
            Program ID to associate with. Must be provided if neither
            `proposal_reference` nor `program_reference` is given.
        proposal_reference : str, optional
            Reference to a proposal; used as an alternative to `program_id`.
        program_reference : str, optional
            Reference to a program label; used as an alternative to `program_id`.

        Returns
        -------
        dict[str, Any]
            The created target and its associated metadata.

        Raises
        ------
        ValueError
            - If no valid program identifier is provided.
            - If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        At least one of `program_id`, `proposal_reference`, or `program_reference`
        must be specified to associate with a valid program.

        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        validate_single_identifier(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
        )

        properties = load_properties(
            properties=properties, from_json=from_json, cls=TargetPropertiesInput
        )

        input_data = CreateTargetInput(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
            set=properties,
        )

        fields = Mutation.create_target(input=input_data).fields(
            CreateTargetResultFields.target().fields(*self._fields()),
        )

        operation_name = "createTarget"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_all(
        self,
        *,
        properties: Optional[TargetPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereTarget] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update one or more targets using a partial or complete
        ``TargetPropertiesInput``.

        Parameters
        ----------
        properties : TargetPropertiesInput, optional
            New values to apply to matching targets. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : WhereTarget, optional
            Query filters to select which targets to update. If omitted, all targets
            are eligible.
        limit : int, optional
            Maximum number of targets to update. If omitted, all matches are updated.
        include_deleted : bool, default=False
            Whether to include soft-deleted targets in the update.

        Returns
        -------
        dict[str, Any]
            A dictionary containing update results and the updated targets.

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
            properties=properties, from_json=from_json, cls=TargetPropertiesInput
        )

        input_data = UpdateTargetsInput(
            set=properties,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )

        fields = Mutation.update_targets(input=input_data).fields(
            UpdateTargetsResultFields.has_more,
            UpdateTargetsResultFields.targets().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )

        operation_name = "updateTargets"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return result[operation_name]

    async def update_by_id(
        self,
        target_id: str,
        *,
        properties: Optional[TargetPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update a single target by its unique identifier.

        Parameters
        ----------
        target_id : str
            Unique identifier of the target. This or ``from_json`` must be
            supplied.
        properties : TargetPropertiesInput, optional
            New values to apply to the target.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted targets in the update.

        Returns
        -------
        dict[str, Any]
            Dictionary containing update result, including updated target data.

        Raises
        ------
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        where = WhereTarget(id=WhereOrderTargetId(eq=target_id))

        results = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            from_json=from_json,
            include_deleted=include_deleted,
        )

        # Since it returns one item, discard the 'matches' and return the item.
        return results["targets"][0]

    async def get_by_id(
        self, target_id: str, *, include_deleted: bool = False
    ) -> dict[str, Any]:
        """
        Fetch a single resource by ID.

        Parameters
        ----------
        target_id : str
            Unique identifier of the target.
        include_deleted : bool, default=False
            Whether to include soft-deleted targets when retrieving.

        Returns
        -------
        dict[str, Any]
            Retrieved data.
        """
        fields = Query.target(target_id=target_id).fields(
            *self._fields(include_deleted=include_deleted)
        )

        operation_name = "target"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereTarget | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Get all targets with optional filtering and pagination.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include deleted resources.
        where : WhereTarget, optional
            Optional filter criteria.
        offset : int, optional
            Cursor-based offset (by ID).
        limit : int, optional
            Maximum number of results.

        Returns
        -------
        dict[str, Any]
            Dictionary with `matches` and `hasMore` keys.
        """
        fields = Query.targets(
            include_deleted=include_deleted, where=where, offset=offset, limit=limit
        ).fields(
            TargetSelectResultFields.has_more,
            TargetSelectResultFields.matches().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )
        operation_name = "targets"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

    async def restore_by_id(self, target_id: str) -> dict[str, Any]:
        """
        Restore a soft-deleted resource by setting its existence to PRESENT.

        Parameters
        ----------
        target_id : str
            Unique identifier of the target.

        Returns
        -------
        dict[str, Any]
            The restore result payload.
        """
        target_properties = TargetPropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            target_id, target_properties=target_properties, include_deleted=True
        )

    async def delete_by_id(self, target_id: str) -> dict[str, Any]:
        """
        Soft-delete a resource by setting its existence to DELETED.

        Parameters
        ----------
        target_id : str
            Unique identifier of the target.

        Returns
        -------
        dict[str, Any]
            The delete result payload.
        """
        target_properties = TargetPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            target_id,
            target_properties=target_properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool = False) -> tuple:
        """Generate the fields to return."""
        return (
            TargetFields.id,
            TargetFields.existence,
            TargetFields.name,
            TargetFields.calibration_role,
            TargetFields.program(include_deleted=include_deleted).fields(
                ProgramFields.id,
                ProgramFields.name,
                ProgramFields.description,
                ProgramFields.existence,
            ),
        )
