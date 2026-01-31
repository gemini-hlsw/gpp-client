"""
Manager for interacting with configuration request resources.
"""

__all__ = ["ConfigurationRequestManager"]

from typing import Any

from gpp_client.api.custom_fields import (
    ConfigurationConditionsFields,
    ConfigurationFields,
    ConfigurationGmosNorthLongSlitFields,
    ConfigurationGmosSouthLongSlitFields,
    ConfigurationObservingModeFields,
    ConfigurationRequestFields,
    ConfigurationRequestSelectResultFields,
    ConfigurationTargetFields,
    CoordinatesFields,
    DeclinationFields,
    RightAscensionFields,
)
from gpp_client.api.custom_queries import Query
from gpp_client.api.enums import ConfigurationRequestStatus
from gpp_client.api.input_types import (
    WhereConfigurationRequest,
    WhereOrderConfigurationRequestStatus,
    WhereOrderProgramId,
    WhereProgram,
)
from gpp_client.managers.base import BaseManager


class ConfigurationRequestManager(BaseManager):
    """
    Manager for interacting with configuration request resources.
    """

    _OP_LIST: str = "configurationRequests"

    @staticmethod
    def _build_where(
        *,
        program_id: str | None,
        status: ConfigurationRequestStatus | None,
        where: WhereConfigurationRequest | None,
    ) -> WhereConfigurationRequest:
        """
        Build a ``WhereConfigurationRequest`` applying explicit overrides.
        """
        built = where.model_copy() if where is not None else WhereConfigurationRequest()

        updates: dict[str, Any] = {}

        if program_id is not None:
            updates["program"] = WhereProgram(id=WhereOrderProgramId(eq=program_id))

        if status is not None:
            updates["status"] = WhereOrderConfigurationRequestStatus(eq=status)

        if updates:
            built = built.model_copy(update=updates)

        return built

    async def get_all(
        self,
        *,
        program_id: str | None = None,
        status: ConfigurationRequestStatus | None = None,
        where: WhereConfigurationRequest | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve all configuration requests with optional filters.

        Parameters
        ----------
        program_id : str, optional
            Program ID to filter by.
        status : ConfigurationRequestStatus, optional
            Status to filter by.
        where : WhereConfigurationRequest, optional
            Filter criteria.
        offset : int, optional
            Cursor offset (by ID).
        limit : int, optional
            Maximum number of items.

        Returns
        -------
        dict[str, Any]
            A dictionary with the results.

        Raises
        ------
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        built_where = self._build_where(
            program_id=program_id, status=status, where=where
        )

        fields = Query.configuration_requests(
            where=built_where, offset=offset, limit=limit
        ).fields(
            ConfigurationRequestSelectResultFields.has_more,
            ConfigurationRequestSelectResultFields.matches().fields(*self._fields()),
        )
        result = await self.client.query(fields, operation_name=self._OP_LIST)

        return self.get_result(result, self._OP_LIST)

    async def get_all_approved_by_program_id(
        self,
        *,
        program_id: str,
        where: WhereConfigurationRequest | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Convenience method for getting approved configuration requests by program ID.

        Parameters
        ----------
        program_id : str, optional
            Program ID to filter by.
        where : WhereConfigurationRequest, optional
            Filter criteria.
        offset : int, optional
            Cursor offset (by ID).
        limit : int, optional
            Maximum number of items.

        Returns
        -------
        dict[str, Any]
            A dictionary with the results.

        Raises
        ------
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        return await self.get_all(
            program_id=program_id,
            status=ConfigurationRequestStatus.APPROVED,
            where=where,
            offset=offset,
            limit=limit,
        )

    @staticmethod
    def _fields() -> tuple:
        """
        Return the GraphQL fields to retrieve for configuration requests.

        Returns
        -------
        tuple
            Field selections for configuration request queries.
        """
        return (
            ConfigurationRequestFields.id,
            ConfigurationRequestFields.status,
            ConfigurationRequestFields.justification,
            ConfigurationRequestFields.applicable_observations,
            ConfigurationRequestFields.configuration().fields(
                ConfigurationFields.conditions().fields(
                    ConfigurationConditionsFields.cloud_extinction,
                    ConfigurationConditionsFields.sky_background,
                    ConfigurationConditionsFields.water_vapor,
                    ConfigurationConditionsFields.image_quality,
                ),
                ConfigurationFields.target().fields(
                    ConfigurationTargetFields.coordinates().fields(
                        CoordinatesFields.ra().fields(
                            RightAscensionFields.hms,
                            RightAscensionFields.hours,
                            RightAscensionFields.degrees,
                        ),
                        CoordinatesFields.dec().fields(
                            DeclinationFields.dms, DeclinationFields.degrees
                        ),
                    )
                ),
                ConfigurationFields.observing_mode().fields(
                    ConfigurationObservingModeFields.instrument,
                    ConfigurationObservingModeFields.mode,
                    ConfigurationObservingModeFields.gmos_north_long_slit().fields(
                        ConfigurationGmosNorthLongSlitFields.grating
                    ),
                    ConfigurationObservingModeFields.gmos_south_long_slit().fields(
                        ConfigurationGmosSouthLongSlitFields.grating
                    ),
                ),
            ),
        )
