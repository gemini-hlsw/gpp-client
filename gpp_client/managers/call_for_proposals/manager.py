"""Resource manager for interacting with the Call for Proposals GraphQL API."""

__all__ = ["CallForProposalsManager"]

from pathlib import Path
from typing import Any, Optional, Union

from ...mixins import (
    CreateMixin,
    DeleteByIdViaBatchMixin,
    GetBatchMixin,
    GetByIdMixin,
    RestoreByIdViaBatchMixin,
    UpdateByIdViaBatchMixin,
)
from ..base_manager import BaseManager
from . import queries


class CallForProposalsManager(
    GetBatchMixin,
    GetByIdMixin,
    CreateMixin,
    UpdateByIdViaBatchMixin,
    DeleteByIdViaBatchMixin,
    RestoreByIdViaBatchMixin,
    BaseManager,
):
    """Manages operations on Call for Proposals resources."""

    default_fields = queries.DEFAULT_FIELDS

    queries = {
        "get_by_id": queries.GET_BY_ID,
        "get_batch": queries.GET_BATCH,
        "update_by_id": queries.UPDATE_BATCH,
        "update_batch": queries.UPDATE_BATCH,
        "get_all": queries.GET_BATCH,
        "get_all_open": queries.GET_BATCH,
        "get_all_closed": queries.GET_BATCH,
        "delete_by_id": queries.UPDATE_BATCH,
        "restore_by_id": queries.UPDATE_BATCH,
    }
    resource_id_field = "callForProposalsId"

    async def create(
        self,
        *,
        type: Optional[str] = None,
        semester: Optional[str] = None,
        active_start: Optional[str] = None,
        active_end: Optional[str] = None,
        coordinate_limits: Optional[dict[str, Any]] = None,
        submission_deadline_default: Optional[str] = None,
        partners: Optional[list[dict[str, Any]]] = None,
        instruments: Optional[list[str]] = None,
        proprietary_months: Optional[int] = None,
        existence: str = "PRESENT",
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Create a new Call for Proposals.

        Parameters
        ----------
        type : str, optional
            The proposal type.
        semester : str, optional
            The semester associated with the call (e.g. '2025A').
        active_start : str, optional
            The start date of the active period (ISO format).
        active_end : str, optional
            The end date of the active period (ISO format).
        coordinate_limits : dict, optional
            Nested coordinate limits per site.
        submission_deadline_default : str, optional
            Default submission deadline timestamp.
        partners : list[dict[str, Any]], optional
            List of partner submission deadline structures.
        instruments : list[str], optional
            Instrument identifiers allowed.
        proprietary_months : int, optional
            Length of proprietary period in months.
        existence : str, default="PRESENT"
            Resource existence state.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            Override return field selection.

        Returns
        -------
        dict[str, Any]
            The created Call for Proposals resource.
        """
        set_values: dict[str, Any] = {
            "type": type,
            "semester": semester,
            "activeStart": str(active_start),
            "activeEnd": str(active_end),
            "existence": existence,
        }

        if coordinate_limits:
            set_values["coordinateLimits"] = coordinate_limits

        if submission_deadline_default:
            set_values["submissionDeadlineDefault"] = submission_deadline_default

        if partners:
            set_values["partners"] = partners

        if instruments:
            set_values["instruments"] = instruments

        if proprietary_months is not None:
            set_values["proprietaryMonths"] = proprietary_months

        return await super().create(
            set_values=set_values, from_json_file=from_json_file, fields=fields
        )

    async def update_by_id(
        self,
        *,
        call_for_proposals_id: str,
        type: Optional[str] = None,
        semester: Optional[str] = None,
        active_start: Optional[str] = None,
        active_end: Optional[str] = None,
        coordinate_limits: Optional[dict[str, Any]] = None,
        submission_deadline_default: Optional[str] = None,
        partners: Optional[list[dict[str, Any]]] = None,
        instruments: Optional[list[str]] = None,
        proprietary_months: Optional[int] = None,
        existence: Optional[str] = None,
        include_deleted: Optional[bool] = None,
        from_json_file: Optional[Union[str, Path]] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Update an existing Call for Proposals by its ID.

        Parameters
        ----------
        call_for_proposals_id : str
            The unique identifier of the Call for Proposals to update.
        type : str
            The proposal type.
        semester : str
            The semester associated with the call (e.g. '2025A').
        active_start : str
            The start date of the active period (ISO format).
        active_end : str
            The end date of the active period (ISO format).
        coordinate_limits : dict[str, Any], optional
            Nested coordinate limits per site.
        submission_deadline_default : str, optional
            Default submission deadline timestamp.
        partners : list[dict[str, Any]], optional
            List of partner submission deadline structures.
        instruments : list[str], optional
            Instrument identifiers allowed.
        proprietary_months : int, optional
            Length of proprietary period in months.
        existence : str, optional
            Resource existence state (default is 'PRESENT').
        include_deleted: bool, optional
            Whether to include deleted resources when updating.
        from_json_file : str or Path, optional
            Path to a JSON file whose keys will override values in `set_values`.
            This only affects the `SET` portion of the mutation.
        fields : str, optional
            Override return field selection.

        Returns
        -------
        dict[str, Any]
            The updated Call for Proposals resource.
        """
        set_values: dict[str, Any] = {}

        if type is not None:
            set_values["type"] = type
        if semester is not None:
            set_values["semester"] = semester
        if active_start is not None:
            set_values["activeStart"] = str(active_start)
        if active_end is not None:
            set_values["activeEnd"] = str(active_end)
        if existence is not None:
            set_values["existence"] = existence
        if coordinate_limits is not None:
            set_values["coordinateLimits"] = coordinate_limits
        if submission_deadline_default is not None:
            set_values["submissionDeadlineDefault"] = submission_deadline_default
        if partners is not None:
            set_values["partners"] = partners
        if instruments is not None:
            set_values["instruments"] = instruments
        if proprietary_months is not None:
            set_values["proprietaryMonths"] = proprietary_months

        if not set_values:
            raise ValueError("At least one field must be provided to update.")

        return await super().update_by_id(
            resource_id=call_for_proposals_id,
            set_values=set_values,
            include_deleted=include_deleted,
            from_json_file=from_json_file,
            fields=fields,
        )

    async def get_all(
        self,
        *,
        include_deleted: Optional[bool] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return all calls for proposals.

        Parameters
        ----------
        include_deleted : bool, optional
            Whether to include deleted records.
        limit : int, optional
            Maximum number of resources to include in the response. If additional
            resources were restored, `hasMore` will be true.
        fields : str, optional
            Override return field selection.

        Returns
        -------
        dict[str, Any]
            Dictionary containing matched results and hasMore flag.
        """
        return await super().get_batch(
            limit=limit, include_deleted=include_deleted, fields=fields
        )

    async def get_all_open(
        self,
        *,
        include_deleted: Optional[bool] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return all open calls for proposals.

        Parameters
        ----------
        include_deleted : bool, optional
            Whether to include deleted records.
        limit : int, optional
            Maximum number of resources to include in the response. If additional
            resources were restored, `hasMore` will be true.
        fields : str, optional
            Override return field selection.

        Returns
        -------
        dict[str, Any]
            Dictionary containing matched results and hasMore flag.
        """
        where = {"isOpen": {"EQ": True}}
        return await super().get_batch(
            where=where, limit=limit, include_deleted=include_deleted, fields=fields
        )

    async def get_all_closed(
        self,
        *,
        include_deleted: Optional[bool] = None,
        limit: Optional[int] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:
        """Return all closed calls for proposals.

        Parameters
        ----------
        include_deleted : bool, optional
            Whether to include deleted records.
        limit : int, optional
            Maximum number of resources to include in the response. If additional
            resources were restored, `hasMore` will be true.
        fields : str, optional
            Override return field selection.

        Returns
        -------
        dict[str, Any]
            Dictionary containing matched results and hasMore flag.
        """
        where = {"isOpen": {"EQ": False}}
        return await super().get_batch(
            where=where, limit=limit, include_deleted=include_deleted, fields=fields
        )
