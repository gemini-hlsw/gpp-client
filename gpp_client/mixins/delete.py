"""Delete mixins for soft-deleting GraphQL resources.

These mixins provide batch and single-resource deletion functionality,
including support for program ID–scoped deletion.
"""

__all__ = ["DeleteBatchMixin", "DeleteByIdViaBatchMixin", "DeleteBatchByProgramIdMixin"]

from typing import Any, Optional

from .utils import create_program_id_filter, build_input_values

_SET_VALUES = {"existence": "DELETED"}


class DeleteBatchMixin:
    """Mixin to soft-delete multiple resources using a custom filter."""

    async def delete_batch(
        self,
        *,
        where: dict[str, Any],
        limit: Optional[int] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Soft-delete multiple resources using a custom `where` filter.

        Parameters
        ----------
        where : dict[str, Any]
            The filter to match resources.
        limit : int, optional
            Maximum number of deleted resources to include in the response. All matching
            resources will be deleted, but only the first `limit` will be returned in
            the GraphQL result. If additional resources were deleted, `hasMore` will be
            true.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The response from the delete mutation.
        """
        input_values = build_input_values(
            set_values=_SET_VALUES,
            where=where,
            limit=limit,
            include_deleted=False,
        )

        query = self.get_query(query_id="delete_batch", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class DeleteByIdViaBatchMixin:
    """Mixin to soft-delete a resource by ID using batch mutation."""

    async def delete_by_id(
        self,
        *,
        resource_id: str,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Soft-delete a single resource by its ID.

        Parameters
        ----------
        resource_id : str
            ID of the resource to delete.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The response from the delete mutation.
        """
        where = {"id": {"EQ": resource_id}}
        input_values = build_input_values(
            set_values=_SET_VALUES,
            limit=1,
            where=where,
            include_deleted=False,
        )

        query = self.get_query(query_id="delete_by_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)


class DeleteBatchByProgramIdMixin:
    """Mixin to soft-delete resources filtered by program ID."""

    async def delete_batch_by_program_id(
        self,
        *,
        program_id: str,
        where: Optional[dict[str, Any]] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Soft-delete resources associated with a program ID.

        Parameters
        ----------
        program_id : str
            The program ID to scope the deletion.
        where : dict[str, Any], optional
            Additional filters to apply.
        limit : int, optional
            Maximum number of deleted resources to include in the response. All matching
            resources will be deleted, but only the first `limit` will be returned in
            the GraphQL result. If additional resources were deleted, `hasMore` will be
            true.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The response from the delete mutation.
        """
        program_filter = create_program_id_filter(program_id)

        if where:
            combined_where = {"AND": [program_filter, where]}
        else:
            combined_where = program_filter

        input_values = build_input_values(
            set_values=_SET_VALUES,
            limit=limit,
            where=combined_where,
            include_deleted=False,
        )

        query = self.get_query(query_id="delete_batch_by_program_id", fields=fields)

        return await self.execute(query=query, input_values=input_values)
