"""Base class for GraphQL resource managers.

This class defines shared behavior for all resource managers including access
to the client, default fields, and dynamic query resolution.

To create your own manager:

1. Define `queries` as a mapping of operation names to GraphQL query templates
using the `{fields}` placeholder.

2. Define `default_fields` with the default selection set.

3. Define `resource_id_field` as the unique identifier key (e.g., "programNoteId").
This is used only for 'GetByIdMixin' for now.

You can optionally override methods from mixins to provide ergonomic interfaces
for common mutations or queries (e.g., `create`, `update_by_id`).

Mixins expect:

- `get_client()` to return a GPPClient instance.
- `get_query(query_id=query_id, fields=fields)` to substitute selection sets into
    templates.
"""

__all__ = ["BaseManager"]

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from ..client import GPPClient


class BaseManager:
    """Base class for GraphQL resource managers.

    Parameters
    ----------
    client : GPPClient
        The initialized client used to execute GraphQL operations.
    """

    default_fields: str
    queries: dict[str, Optional[str]] = {
        "get_batch": None,
        "get_batch_by_program_id": None,
        "get_by_id": None,
        "restore_by_id": None,
        "restore_by_program_id": None,
        "update_by_id": None,
        "update_by_id_via_batch": None,
        "update_batch": None,
        "update_batch_by_program_id": None,
        "create": None,
        "delete_batch": None,
        "delete_by_id": None,
        "delete_batch_by_program_id": None,
    }

    # Only needed if using 'GetByIdMixin'.
    resource_id_field: Optional[str]

    _client: "GPPClient"

    def __init__(self, client: "GPPClient") -> None:
        self._client = client
        self._submanagers: dict[str, BaseManager] = {}
        self.register_submanagers()

    @property
    def registered_queries(self) -> set[str]:
        """Return a set of registered query IDs.

        This includes only the keys from `queries` that are not `None`.

        Returns
        -------
        set[str]
            The set of query IDs with registered templates.
        """
        return {k for k, v in self.queries.items() if v is not None}

    @property
    def submanagers(self) -> dict[str, "BaseManager"]:
        return self._submanagers

    def get_client(self) -> "GPPClient":
        """Return the GraphQL client.

        Returns
        -------
        GPPClient
            The active client instance.
        """
        return self._client

    def get_query(self, *, query_id: str, fields: Optional[str] = None) -> str:
        """Resolve and return a formatted query template.

        Parameters
        ----------
        query_id : str
            The name of the query to resolve.
        fields : str, optional
            Custom fields to include in the query response. If not provided,
            `default_fields` is used.

        Returns
        -------
        str
            The formatted GraphQL query string.

        Raises
        ------
        ValueError
            If the query ID is not defined in the `queries` dict.
        """
        query_template = self.queries.get(query_id)
        if query_template is None:
            raise ValueError(
                f"{self.__class__.__name__} does not define a query for: '{query_id}'"
            )
        # Substitute in fields.
        return query_template.replace("{fields}", fields or self.get_default_fields())

    def get_resource_id_field(self) -> str:
        """Return the name of the resource ID field. Currently only needed for
        'GetByIdMixin'.

        Returns
        -------
        str
            The resource ID field name.

        Raises
        ------
        NotImplementedError
            If `resource_id_field` is not properly defined.
        """
        if not hasattr(self, "resource_id_field") or not isinstance(
            self.resource_id_field, str
        ):
            raise NotImplementedError(
                f"{self.__class__.__name__} must define `resource_id_field` as a "
                "string to use the 'GetByIdMixin'."
            )
        return self.resource_id_field

    def get_default_fields(self) -> str:
        """Return the default fields used in queries.

        Returns
        -------
        str
            A string of default GraphQL fields to be selected.

        Raises
        ------
        NotImplementedError
            If `default_fields` is not properly defined.
        """
        if not hasattr(self, "default_fields") or not isinstance(
            self.default_fields, str
        ):
            raise NotImplementedError(
                f"{self.__class__.__name__} must define `default_fields` as a string."
            )
        return self.default_fields

    def register_submanagers(self) -> None:
        """Hook for subclasses to register their submanagers."""
        pass

    def register_submanager(self, name: str, manager: "BaseManager") -> None:
        """Register a submanager as an attribute (e.g., self.reference)."""
        self._submanagers[name] = manager
        setattr(self, name, manager)

    def get_submanager(self, name: str) -> Optional["BaseManager"]:
        """Access a submanager by name (e.g., 'reference')."""
        return self._submanagers.get(name)
