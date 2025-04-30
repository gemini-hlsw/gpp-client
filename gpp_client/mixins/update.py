"""
This module provides reusable mixins for updating resources via GraphQL,
supporting batch updates, updates by ID, and updates filtered by program ID.
"""

__all__ = [
    "UpdateByIdMixin",
    "UpdateByIdViaBatchMixin",
    "UpdateBatchMixin",
    "UpdateBatchByProgramIdMixin",
]

from pathlib import Path
from typing import Any, Optional, Union

from .utils import create_program_id_filter, merge_set_values, build_input_values


class UpdateByIdMixin:
    """Provides update_by_id for updating a resource by identifier."""

    async def update_by_id(
        self,
        *,
        set_values: dict[str, Any],
        identifier: Optional[dict[str, Any]] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Execute an update mutation on a single resource.

        Parameters
        ----------
        set_values : dict[str, Any]
            The `SET` block of values to define the resource.
        identifier : dict[str, Any], optional
            One or more GraphQL identifiers (e.g., {"programId": "p-2025A-001"}).
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            Optional fields to return in the mutation response. Defaults to `default_fields`.

        Returns
        -------
        dict[str, Any]
            The result of the mutation.

        Raises
        ------
        ValueError
            If the file is invalid, or input is incomplete.
        """
        set_values = merge_set_values(set_values, from_json_file)
        input_values = build_input_values(set_values=set_values, identifier=identifier)

        query = self.get_query(query_id="update_by_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class UpdateByIdViaBatchMixin:
    """Provides an update_by_id method using a batch-style update query."""

    async def update_by_id(
        self,
        *,
        resource_id: str,
        set_values: dict[str, Any],
        include_deleted: Optional[bool] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update a single resource by its ID via batch method.

        Parameters
        ----------
        resource_id : str
            The ID of the resource to update.
        set_values : dict[str, Any]
            Fields to update on the resource.
        include_deleted : bool, optional
            Whether to include soft-deleted records in the update.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The updated resource.
        """
        set_values = merge_set_values(set_values, from_json_file)
        where = {"id": {"EQ": resource_id}}
        input_values = build_input_values(
            set_values=set_values, where=where, limit=1, include_deleted=include_deleted
        )

        query = self.get_query(query_id="update_by_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class UpdateBatchMixin:
    """Provides update_batch for updating multiple resources using a where clause."""

    async def update_batch(
        self,
        *,
        set_values: dict[str, Any],
        where: dict[str, Any],
        limit: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update multiple resources matching a given filter.

        Parameters
        ----------
        set_values : dict[str, Any]
            Fields to update in each matching resource.
        where : dict[str, Any]
            The filter for selecting resources to update.
        limit : int, optional
            Maximum number of updated resources to include in the response. All matching
            resources will be updated, but only the first `limit` will be returned in
            the GraphQL result. If additional resources were updated, `hasMore` will be
            true.
        include_deleted : bool, optional
            Whether to include soft-deleted records in the update.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The updated resources and `hasMore` flag.
        """
        set_values = merge_set_values(set_values, from_json_file)
        input_values = build_input_values(
            set_values=set_values,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )

        query = self.get_query(query_id="update_batch", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class UpdateBatchByProgramIdMixin:
    """Provides update_batch_by_program_id for filtering updates by program."""

    async def update_batch_by_program_id(
        self,
        *,
        program_id: str,
        set_values: dict[str, Any],
        where: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update resources matching a program ID and optional filters.

        Parameters
        ----------
        program_id : str
            The program ID to match.
        set_values : dict[str, Any]
            Fields to update in matching resources.
        where : dict[str, Any], optional
            Additional filter conditions.
        limit : int, optional
            Maximum number of updated resources to include in the response. All matching
            resources will be updated, but only the first `limit` will be returned in
            the GraphQL result. If additional resources were updated, `hasMore` will be
            true.
        include_deleted : bool, optional
            Whether to include soft-deleted records in the update.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The updated resources and `hasMore` flag.
        """
        set_values = merge_set_values(set_values, from_json_file)
        program_filter = create_program_id_filter(program_id)

        # Combine the wheres if given.
        if where:
            combined_where = {"AND": [program_filter, where]}
        else:
            combined_where = program_filter

        input_values = build_input_values(
            set_values=set_values,
            where=combined_where,
            limit=limit,
            include_deleted=include_deleted,
        )
        query = self.get_query(query_id="update_batch_by_program_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)
