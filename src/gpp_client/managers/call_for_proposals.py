"""
Manager for interacting with call for proposals resources.
"""

__all__ = ["CallForProposalsManager"]

from pathlib import Path
from typing import Any, Optional

from gpp_client.api.custom_fields import (
    CallForProposalsFields,
    CallsForProposalsSelectResultFields,
    CreateCallForProposalsResultFields,
    DateIntervalFields,
    UpdateCallsForProposalsResultFields,
)
from gpp_client.api.custom_mutations import Mutation
from gpp_client.api.custom_queries import Query
from gpp_client.api.enums import Existence
from gpp_client.api.input_types import (
    CallForProposalsPropertiesInput,
    CreateCallForProposalsInput,
    UpdateCallsForProposalsInput,
    WhereCallForProposals,
    WhereOrderCallForProposalsId,
)
from gpp_client.managers.base import BaseManager


class CallForProposalsManager(BaseManager):
    """
    Manager for interacting with call for proposals resources.
    """

    _OP_CREATE: str = "createCallForProposals"
    _OP_UPDATE: str = "updateCallsForProposals"
    _OP_GET: str = "callForProposals"
    _OP_LIST: str = "callsForProposals"

    @staticmethod
    def _build_where_for_id(*, call_for_proposals_id: str) -> WhereCallForProposals:
        """Build a ``WhereCallForProposals`` filter for a ``call_for_proposals_id``."""
        return WhereCallForProposals(
            id=WhereOrderCallForProposalsId(eq=call_for_proposals_id)
        )

    async def create(
        self,
        *,
        properties: Optional[CallForProposalsPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Create a new call for proposals.

        Parameters
        ----------
        properties : CallForProposalsPropertiesInput, optional
            Full definition of the call for proposals to create. This or ``from_json``
            must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.

        Returns
        -------
        dict[str, Any]
            The created call for proposals.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``GPPValidationError``.
        """
        properties = self.load_properties(
            properties=properties,
            from_json=from_json,
            cls=CallForProposalsPropertiesInput,
        )

        input_data = CreateCallForProposalsInput(set=properties)

        fields = Mutation.create_call_for_proposals(input=input_data).fields(
            CreateCallForProposalsResultFields.call_for_proposals().fields(
                *self._fields()
            ),
        )

        result = await self.client.mutation(fields, operation_name=self._OP_CREATE)
        return self.get_result(result, self._OP_CREATE)

    async def update_all(
        self,
        *,
        properties: Optional[CallForProposalsPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereCallForProposals] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update multiple calls for proposals matching the given filter.

        Parameters
        ----------
        properties : CallForProposalsPropertiesInput, optional
            Values to set on the matching calls for proposals. This or ``from_json``
            must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : WhereProgram, optional
            Filter to determine which calls for proposals to update.
        limit : int, optional
            Maximum number of calls for proposals to update.
        include_deleted : bool, default=False
            Whether to include soft-deleted calls for proposals.

        Returns
        -------
        dict[str, Any]
            Update result and updated calls for proposals.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``GPPValidationError``.
        """
        properties = self.load_properties(
            properties=properties,
            from_json=from_json,
            cls=CallForProposalsPropertiesInput,
        )

        input_data = UpdateCallsForProposalsInput(
            set=properties,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )

        fields = Mutation.update_calls_for_proposals(input=input_data).fields(
            UpdateCallsForProposalsResultFields.has_more,
            UpdateCallsForProposalsResultFields.calls_for_proposals().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )

        result = await self.client.mutation(fields, operation_name=self._OP_UPDATE)
        return self.get_result(result, self._OP_UPDATE)

    async def update_by_id(
        self,
        call_for_proposals_id: str,
        *,
        properties: Optional[CallForProposalsPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update a single call for proposals by its ID.

        Parameters
        ----------
        call_for_proposals_id : str
            Unique identifier of the call for proposals to update.
        properties : CallForProposalsPropertiesInput, optional
            New values to apply. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted calls for proposals in the update.

        Returns
        -------
        dict[str, Any]
            The updated call for proposals.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``GPPValidationError``.
        """
        where = self._build_where_for_id(call_for_proposals_id=call_for_proposals_id)

        results = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            from_json=from_json,
            include_deleted=include_deleted,
        )

        # Since it returns one item, discard the 'matches' and return the item.
        return self.get_single_result(results, self._OP_LIST)

    async def get_by_id(
        self, call_for_proposals_id: str, *, include_deleted: bool = False
    ) -> dict[str, Any]:
        """
        Fetch a single call for proposals by its ID.

        Parameters
        ----------
        call_for_proposals_id : str
            Unique identifier of the call for proposals.
        include_deleted : bool, default=False
            Whether to include deleted entries in the lookup.

        Returns
        -------
        dict[str, Any]
            Retrieved call for proposals.

        Raises
        ------
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        fields = Query.call_for_proposals(
            call_for_proposals_id=call_for_proposals_id
        ).fields(*self._fields(include_deleted=include_deleted))

        result = await self.client.query(fields, operation_name=self._OP_GET)
        return self.get_result(result, self._OP_GET)

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereCallForProposals | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Fetch all calls for proposals with optional filters and pagination.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include deleted entries.
        where : WhereCallForProposals, optional
            Optional filtering clause.
        offset : int, optional
            Pagination offset.
        limit : int, optional
            Maximum number of results.

        Returns
        -------
        dict[str, Any]
            Dictionary with `matches` and `hasMore`.

        Raises
        ------
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        fields = Query.calls_for_proposals(
            include_deleted=include_deleted, where=where, offset=offset, limit=limit
        ).fields(
            CallsForProposalsSelectResultFields.has_more,
            CallsForProposalsSelectResultFields.matches().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )
        result = await self.client.query(fields, operation_name=self._OP_LIST)
        return self.get_result(result, self._OP_LIST)

    async def restore_by_id(self, call_for_proposals_id: str) -> dict[str, Any]:
        """
        Restore a soft-deleted call for proposals.

        Parameters
        ----------
        call_for_proposals_id : str
            Unique identifier of the call for proposals.

        Returns
        -------
        dict[str, Any]
            The restored call for proposals.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        properties = CallForProposalsPropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            call_for_proposals_id, properties=properties, include_deleted=True
        )

    async def delete_by_id(self, call_for_proposals_id: str) -> dict[str, Any]:
        """
        Soft-delete a call for proposals.

        Parameters
        ----------
        call_for_proposals_id : str
            Unique identifier of the call for proposals.

        Returns
        -------
        dict[str, Any]
            The deleted call for proposals payload.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        properties = CallForProposalsPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            call_for_proposals_id,
            properties=properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool = False) -> tuple:
        """
        Return the GraphQL fields to retrieve for a call for proposals.

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
            CallForProposalsFields.id,
            CallForProposalsFields.title,
            CallForProposalsFields.type,
            CallForProposalsFields.semester,
            CallForProposalsFields.active().fields(
                DateIntervalFields.start, DateIntervalFields.end
            ),
            CallForProposalsFields.submission_deadline_default,
            CallForProposalsFields.instruments,
            CallForProposalsFields.existence,
        )
