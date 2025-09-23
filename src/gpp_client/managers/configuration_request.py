__all__ = ["ConfigurationRequestManager"]

from typing import Any

from ..api.custom_fields import (
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
from ..api.custom_queries import Query
from ..api.enums import ConfigurationRequestStatus
from ..api.input_types import (
    WhereConfigurationRequest,
    WhereOrderConfigurationRequestStatus,
    WhereOrderProgramId,
    WhereProgram,
)
from .base import BaseManager


class ConfigurationRequestManager(BaseManager):
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
        """
        # Start with user-provided where, or an empty one
        where = where or WhereConfigurationRequest()

        # Apply overrides
        if program_id is not None:
            where.program = WhereProgram(id=WhereOrderProgramId(eq=program_id))

        if status is not None:
            where.status = WhereOrderConfigurationRequestStatus(eq=status)

        fields = Query.configuration_requests(
            where=where, offset=offset, limit=limit
        ).fields(
            ConfigurationRequestSelectResultFields.has_more,
            ConfigurationRequestSelectResultFields.matches().fields(*self._fields()),
        )
        operation_name = "configurationRequests"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

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
