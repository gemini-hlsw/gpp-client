"""Restore mixins for soft-deleted GraphQL resources.

This module provides reusable mixins to restore resources by ID or in batch
based on a program ID, using a batch-style update mutation to set `existence`
to "PRESENT".
"""

__all__ = ["RestoreByIdViaBatchMixin", "RestoreBatchByProgramIdMixin"]

from typing import Any, Optional

from .utils import create_program_id_filter, build_input_values

_SET_VALUES = {"existence": "PRESENT"}


class RestoreByIdViaBatchMixin:
    """Restore a single resource by ID using batch mutation."""

    async def restore_by_id(
        self,
        *,
        resource_id: str,
        include_deleted: bool = True,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Restore a single resource by its ID.

        Parameters
        ----------
        resource_id : str
            The unique ID of the resource to restore.
        include_deleted : bool, default=True
            Whether to include already-deleted records.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The restored resource result.
        """
        where = {"id": {"EQ": resource_id}}

        input_values = build_input_values(
            set_values=_SET_VALUES,
            where=where,
            limit=1,
            include_deleted=include_deleted,
        )

        query = self.get_query(query_id="restore_by_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class RestoreBatchByProgramIdMixin:
    """Restore a batch of resources associated with a specific program ID."""

    async def restore_batch_by_program_id(
        self,
        *,
        program_id: str,
        where: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        include_deleted: bool = True,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Restore multiple resources linked to a program.

        Parameters
        ----------
        program_id : str
            The program ID to match.
        where : dict[str, Any], optional
            Additional filters to apply alongside the program ID.
        limit : int, optional
            Maximum number of restored resources to include in the response. All 
            matching resources will be restored, but only the first `limit` will be 
            returned in the GraphQL result. If additional resources were restored, 
            `hasMore` will be true.
        include_deleted : bool, default=True
            Whether to include already-deleted resources.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The restored resources and metadata.
        """
        program_filter = create_program_id_filter(program_id)

        if where:
            combined_where = {"AND": [program_filter, where]}
        else:
            combined_where = program_filter

        input_values = build_input_values(
            set_values=_SET_VALUES,
            where=combined_where,
            limit=limit,
            include_deleted=include_deleted,
        )

        query = self.get_query(query_id="restore_batch_by_program_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)
