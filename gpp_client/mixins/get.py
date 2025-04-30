"""Get mixins for retrieving GraphQL resources by ID or batch.

This module provides reusable mixins to support fetching resources
by ID, by filters, or in batch by program ID using GraphQL queries.
"""

__all__ = ["GetByIdMixin", "GetBatchMixin", "GetBatchByProgramIdMixin"]

from typing import Any, Optional

from .utils import create_program_id_filter, build_selector_values


class GetByIdMixin:
    """Mixin to fetch a single resource by ID or advanced identifier dictionary."""

    async def get_by_id(
        self,
        *,
        resource_id: Optional[str] = None,
        fields: Optional[str] = None,
        _identifier: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Fetch a single resource by ID or by an identifier dictionary.

        Parameters
        ----------
        resource_id : str, optional
            The unique ID value for the resource. (Normal usage)
        fields : str, optional
            Fields to return in the response.
        _identifier : dict[str, Any], optional
            A dictionary of selector fields for resources requiring multiple
            identifiers. Intended for advanced usage by developers.

        Returns
        -------
        dict[str, Any]
            The resource data.

        Raises
        ------
        ValueError
            If neither or both of 'resource_id' and '_identifier' are provided.
        """
        if bool(resource_id) == bool(_identifier):
            raise ValueError(
                "Exactly one of resource_id` or `_identifier` must be provided."
            )

        if resource_id is not None:
            resource_id_field = self.get_resource_id_field()
            identifier = {resource_id_field: resource_id}
        else:
            identifier = _identifier

        selector_values = build_selector_values(identifier=identifier)

        query = self.get_query(query_id="get_by_id", fields=fields)

        return await self.execute(query=query, selector_values=selector_values)


class GetBatchMixin:
    """Mixin to fetch multiple resources based on filters."""

    async def get_batch(
        self,
        *,
        where: Optional[dict[str, Any]] = None,
        offset: Optional[str] = None,
        limit: Optional[int] = None,
        include_deleted: Optional[bool] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Fetch a batch of resources using filter expressions.

        Parameters
        ----------
        where : dict[str, Any], optional
            Filter expression to match resources.
        offset : str, optional
            Pagination cursor.
        limit : int, optional
            Maximum number of resources to include in the response. If additional
            resources were restored, `hasMore` will be true.
        include_deleted : bool, optional
            Whether to include soft-deleted entries.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The batch query result.
        """
        selector_values = build_selector_values(
            where=where, offset=offset, limit=limit, include_deleted=include_deleted
        )

        query = self.get_query(query_id="get_batch", fields=fields)

        return await self.execute(query=query, selector_values=selector_values)


class GetBatchByProgramIdMixin:
    """Mixin to fetch multiple resources scoped to a specific program."""

    async def get_batch_by_program_id(
        self,
        *,
        program_id: str,
        where: Optional[dict[str, Any]] = None,
        include_deleted: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Fetch a batch of resources linked to a specific program.

        Parameters
        ----------
        program_id : str
            The program ID to filter on.
        where : dict[str, Any], optional
            Additional filters to apply.
        include_deleted : bool, optional
            Whether to include soft-deleted entries.
        limit : int, optional
            Maximum number of resources to include in the response. If additional
            resources were restored, `hasMore` will be true.
        offset : str, optional
            Pagination offset.
        fields : str, optional
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            Query result for the filtered program.
        """
        program_filter = create_program_id_filter(program_id)

        if where:
            combined_where = {"AND": [program_filter, where]}
        else:
            combined_where = program_filter

        selector_values = build_selector_values(
            where=combined_where,
            limit=limit,
            offset=offset,
            include_deleted=include_deleted,
        )

        query = self.get_query(query_id="get_batch_by_program_id", fields=fields)

        return await self.execute(query=query, selector_values=selector_values)
