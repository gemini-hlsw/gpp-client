"""Create mixin for GraphQL resources.

This module provides functionality to create new resources using a standard
GraphQL `create` mutation pattern.
"""

__all__ = ["CreateMixin"]

from typing import Any, Optional


async def _create(
    *, client: Any, query: str, input_values: dict[str, Any]
) -> dict[str, Any]:
    """Helper to perform a create mutation.

    Parameters
    ----------
    client : Any
        The GraphQL client instance.
    query : str
        The GraphQL mutation string with `{fields}` already substituted.
    input_values : dict[str, Any]
        The full input dictionary to pass under the `input` variable.

    Returns
    -------
    dict[str, Any]
        The GraphQL response for the newly created resource.
    """
    return await client._execute(query=query, variables={"input": input_values})


class CreateMixin:
    """Mixin to create a new resource using a GraphQL mutation."""

    async def create(
        self, *, input_values: dict[str, Any], fields: Optional[str] = None
    ) -> dict[str, Any]:
        """Create a new resource via a GraphQL mutation.

        Parameters
        ----------
        input_values : dict[str, Any]
            The full input dictionary to pass to the GraphQL mutation.
        fields : str, optional
            Optional fields to return in the mutation response. Defaults to `default_fields`.

        Returns
        -------
        dict[str, Any]
            The GraphQL response for the newly created resource.
        """
        client = self.get_client()
        query = self.get_query(query_id="create", fields=fields)

        return await _create(client=client, query=query, input_values=input_values)