"""Create mixin for GraphQL resources.

This module provides functionality to create new resources using a standard
GraphQL `create` mutation pattern.
"""

__all__ = ["CreateMixin"]

from pathlib import Path
from typing import Any, Optional, Union
from .utils import merge_set_values, build_input_values


class CreateMixin:
    """Mixin to create a new resource using a GraphQL mutation."""

    async def create(
        self,
        *,
        set_values: dict[str, Any],
        identifier: Optional[dict[str, Any]] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new resource via a GraphQL mutation.

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
            The fields to return in the response.

        Returns
        -------
        dict[str, Any]
            The GraphQL response for the newly created resource.

        Raises
        ------
        ValueError
            If the file is invalid, or input is incomplete.
        """
        set_values = merge_set_values(set_values, from_json_file)
        input_values = build_input_values(set_values=set_values, identifier=identifier)

        query = self.get_query(query_id="create", fields=fields)

        return await self.execute(query=query, input_values=input_values)
