__all__ = ["ObservationManager"]

import logging
from pathlib import Path
from typing import Any, Optional

from gpp_client.api.custom_fields import (
    AirMassRangeFields,
    CalculatedObservationWorkflowFields,
    CloneObservationResultFields,
    ConstraintSetFields,
    CoordinatesFields,
    CreateObservationResultFields,
    DeclinationFields,
    ElevationRangeFields,
    GmosNorthLongSlitFields,
    GmosSouthLongSlitFields,
    HourAngleRangeFields,
    NonsiderealFields,
    ObservationFields,
    ObservationReferenceFields,
    ObservationSelectResultFields,
    ObservingModeFields,
    OffsetQFields,
    ProgramFields,
    ProperMotionDeclinationFields,
    ProperMotionFields,
    ProperMotionRAFields,
    RightAscensionFields,
    ScienceRequirementsFields,
    SiderealFields,
    TargetEnvironmentFields,
    TargetFields,
    TimeSpanFields,
    TimingWindowEndAfterFields,
    TimingWindowEndAtFields,
    TimingWindowFields,
    TimingWindowRepeatFields,
    UpdateObservationsResultFields,
    WavelengthFields,
    Flamingos2LongSlitFields,
    TelluricTypeFields,
    ExposureTimeModeFields,
    SignalToNoiseExposureTimeModeFields,
    TimeAndCountExposureTimeModeFields,
    OffsetFields,
    OffsetPFields,
    Flamingos2LongSlitAcquisitionFields,
)
from gpp_client.api.custom_mutations import Mutation
from gpp_client.api.custom_queries import Query
from gpp_client.api.enums import Existence
from gpp_client.api.input_types import (
    CloneObservationInput,
    CreateObservationInput,
    ObservationPropertiesInput,
    UpdateObservationsInput,
    WhereObservation,
    WhereObservationReference,
    WhereOrderObservationId,
    WhereString,
)
from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)


class ObservationManager(BaseManager):
    async def clone(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
        properties: Optional[ObservationPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Clone an existing observation to create a new one.

        Parameters
        ----------
        observation_id : str, optional
            Unique internal ID of the observation to clone.
        observation_reference : str, optional
            Human-readable reference label (e.g., "G-2025A-1234-Q-0001") of the observation to clone.
        properties : ObservationPropertiesInput, optional
            Properties to override in the cloned observation. This or ``from_json`` may be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the JSON data.

        Returns
        -------
        dict[str, Any]
            A dictionary containing details of the original and new cloned observations.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.

        Notes
        -----
        Exactly one of `observation_id` or `observation_reference` must be provided to
        identify the observation to clone. Additionally, either `properties` or
        `from_json` may be supplied to specify overrides for the cloned observation.
        """
        logger.debug(
            "Cloning observation from observation with ID: %s or reference: %s",
            observation_id,
            observation_reference,
        )
        self.validate_single_identifier(
            observation_id=observation_id, observation_reference=observation_reference
        )

        properties = self.load_properties(
            properties=properties, from_json=from_json, cls=ObservationPropertiesInput
        )

        input_data = CloneObservationInput(
            observation_id=observation_id,
            observation_reference=observation_reference,
            set=properties,
        )
        fields = Mutation.clone_observation(input=input_data).fields(
            CloneObservationResultFields.original_observation().fields(
                # Only a few fields from the original are returned.
                ObservationFields.id,
                ObservationFields.existence,
                ObservationFields.reference().fields(ObservationReferenceFields.label),
            ),
            CloneObservationResultFields.new_observation().fields(*self._fields()),
        )

        operation_name = "cloneObservation"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def create(
        self,
        *,
        properties: Optional[ObservationPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        program_id: Optional[str] = None,
        proposal_reference: Optional[str] = None,
        program_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Create a new observation under a specified program.

        Parameters
        ----------
        properties : ObservationPropertiesInput, optional
            Observation definition to use in creation. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        program_id : str, optional
            Direct program identifier. Must be provided if `proposal_reference` and
            `program_reference` are omitted.
        proposal_reference : str, optional
            Proposal label alternative to `program_id`.
        program_reference : str, optional
            Program label alternative to `program_id`.

        Returns
        -------
        dict[str, Any]
            The created observation and its metadata.

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
        logger.debug(
            "Creating a new observation under a program ID: %s, proposal reference: %s, or program reference: %s",
            program_id,
            proposal_reference,
            program_reference,
        )

        self.validate_single_identifier(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
        )

        properties = self.load_properties(
            properties=properties, from_json=from_json, cls=ObservationPropertiesInput
        )

        input_data = CreateObservationInput(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
            set=properties,
        )

        fields = Mutation.create_observation(input=input_data).fields(
            CreateObservationResultFields.observation().fields(*self._fields()),
        )

        operation_name = "createObservation"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def update_all(
        self,
        *,
        properties: Optional[ObservationPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        where: Optional[WhereObservation] = None,
        limit: Optional[int] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update one or more observations with new properties.

        Parameters
        ----------
        properties : ObservationPropertiesInput, optional
            Fields to update. This or ``from_json`` must be supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        where : WhereObservation, optional
            Filter expression to limit which observations are updated.
        limit : int, optional
            Maximum number of observations to update.
        include_deleted : bool, default=False
            Whether to include soft-deleted observations.

        Returns
        -------
        dict[str, Any]
            The update result and updated records.

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
        logger.debug("Updating observation(s)")
        properties = self.load_properties(
            properties=properties, from_json=from_json, cls=ObservationPropertiesInput
        )

        input_data = UpdateObservationsInput(
            set=properties,
            where=where,
            limit=limit,
            include_deleted=include_deleted,
        )

        fields = Mutation.update_observations(input=input_data).fields(
            UpdateObservationsResultFields.has_more,
            UpdateObservationsResultFields.observations().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )

        operation_name = "updateObservations"
        result = await self.client.mutation(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def update_by_id(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
        properties: Optional[ObservationPropertiesInput] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Update a single observation by ID or reference.

        Parameters
        ----------
        observation_id : str, optional
            Unique internal ID of the observation.
        observation_reference : str, optional
            Human-readable reference label (e.g., "G-2025A-1234-Q-0001").
        properties : ObservationPropertiesInput, optional
            New values to apply to the observation. This or ``from_json`` must be
            supplied.
        from_json : str | Path | dict[str, Any], optional
            JSON representation of the properties. May be a path-like object
            (``str`` or ``Path``) to a JSON file, or a ``dict`` already containing the
            JSON data.
        include_deleted : bool, default=False
            Whether to include soft-deleted observations in the match.

        Returns
        -------
        dict[str, Any]
            The updated observation.

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
        logger.debug(
            "Updating observation by ID: %s or reference: %s",
            observation_id,
            observation_reference,
        )
        self.validate_single_identifier(
            observation_id=observation_id,
            observation_reference=observation_reference,
        )

        if observation_id:
            where = WhereObservation(id=WhereOrderObservationId(eq=observation_id))
        else:
            where = WhereObservation(
                reference=WhereObservationReference(
                    label=WhereString(eq=observation_reference)
                )
            )

        result = await self.update_all(
            where=where,
            limit=1,
            properties=properties,
            include_deleted=include_deleted,
            from_json=from_json,
        )

        return self.get_single_result(result, "observations")

    async def get_by_id(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
        include_deleted: bool = False,
    ) -> dict[str, Any]:
        """
        Fetch a single observation by ID or reference.

        This method retrieves a single observation using either the internal ID or
        the reference label. Exactly one of `observation_id` or `observation_reference`
        must be provided.

        Parameters
        ----------
        observation_id : str, optional
            The unique internal identifier of the observation.
        observation_reference : str, optional
            The human-readable reference label (e.g., "G-2024B-1234-Q-0001").
        include_deleted : bool, default=False
            Whether to include soft-deleted observations in the query.

        Returns
        -------
        dict[str, Any]
            The retrieved observation.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug(
            "Fetching observation by ID: %s or reference: %s",
            observation_id,
            observation_reference,
        )
        self.validate_single_identifier(
            observation_id=observation_id, observation_reference=observation_reference
        )

        fields = Query.observation(
            observation_id=observation_id, observation_reference=observation_reference
        ).fields(*self._fields(include_deleted=include_deleted))

        operation_name = "observation"
        result = await self.client.query(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def get_all(
        self,
        *,
        include_deleted: bool = False,
        where: WhereObservation | None = None,
        offset: int | None = None,
        limit: int | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve all observations with optional filters.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include soft-deleted observations.
        where : WhereObservation, optional
            Filter criteria.
        offset : int, optional
            Cursor offset (by ID).
        limit : int, optional
            Maximum number of observations.

        Returns
        -------
        dict[str, Any]
            A dictionary with the results.

        Raises
        ------
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug("Retrieving observation(s)")
        fields = Query.observations(
            include_deleted=include_deleted, where=where, offset=offset, limit=limit
        ).fields(
            ObservationSelectResultFields.has_more,
            ObservationSelectResultFields.matches().fields(
                *self._fields(include_deleted=include_deleted)
            ),
        )
        operation_name = "observations"
        result = await self.client.query(fields, operation_name=operation_name)
        return self.get_result(result, operation_name)

    async def restore_by_id(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Restore a soft-deleted observation using ID or reference.

        Parameters
        ----------
        observation_id : str, optional
            Unique internal ID of the observation to restore.
        observation_reference : str, optional
            Human-readable reference label (e.g., "G-2025A-1234-Q-0001").

        Returns
        -------
        dict[str, Any]
            The restored observation with `existence` set to PRESENT.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug(
            "Restoring observation with ID: %s or reference: %s",
            observation_id,
            observation_reference,
        )
        properties = ObservationPropertiesInput(existence=Existence.PRESENT)
        return await self.update_by_id(
            observation_id=observation_id,
            observation_reference=observation_reference,
            properties=properties,
            include_deleted=True,
        )

    async def delete_by_id(
        self,
        *,
        observation_id: Optional[str] = None,
        observation_reference: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Soft-delete an observation using ID or reference.

        Parameters
        ----------
        observation_id : str, optional
            Unique internal ID of the observation to delete.
        observation_reference : str, optional
            Human-readable reference label (e.g., "G-2025A-1234-Q-0001").

        Returns
        -------
        dict[str, Any]
            The deleted observation with `existence` set to DELETED.

        Raises
        ------
        GPPValidationError
            If a validation error occurs.
        GPPClientError
            If an unexpected error occurs unpacking the response.
        """
        logger.debug(
            "Deleting observation with ID: %s or reference: %s",
            observation_id,
            observation_reference,
        )
        properties = ObservationPropertiesInput(existence=Existence.DELETED)
        return await self.update_by_id(
            observation_id=observation_id,
            observation_reference=observation_reference,
            properties=properties,
            include_deleted=False,
        )

    @staticmethod
    def _fields(include_deleted: bool = False) -> tuple:
        """
        Return the GraphQL fields to retrieve for observations.

        Parameters
        ----------
        include_deleted : bool, default=False
            Whether to include deleted fields in nested lookups.

        Returns
        -------
        tuple
            Field selections for observation queries.
        """
        return (
            ObservationFields.id,
            ObservationFields.existence,
            ObservationFields.reference().fields(ObservationReferenceFields.label),
            ObservationFields.calibration_role,
            ObservationFields.instrument,
            ObservationFields.observer_notes,
            ObservationFields.title,
            ObservationFields.subtitle,
            ObservationFields.program().fields(
                ProgramFields.id,
                ProgramFields.name,
                ProgramFields.existence,
            ),
            ObservationFields.science_requirements().fields(
                ScienceRequirementsFields.mode
            ),
            ObservationFields.science_band,
            ObservationFields.workflow().fields(
                CalculatedObservationWorkflowFields.state
            ),
            ObservationFields.observing_mode().fields(
                ObservingModeFields.instrument,
                ObservingModeFields.mode,
                ObservingModeFields.gmos_north_long_slit().fields(
                    GmosNorthLongSlitFields.grating,
                    GmosNorthLongSlitFields.filter,
                    GmosNorthLongSlitFields.fpu,
                    GmosNorthLongSlitFields.central_wavelength().fields(
                        WavelengthFields.nanometers
                    ),
                    GmosNorthLongSlitFields.spatial_offsets().fields(
                        OffsetQFields.arcseconds
                    ),
                ),
                ObservingModeFields.gmos_south_long_slit().fields(
                    GmosSouthLongSlitFields.grating,
                    GmosSouthLongSlitFields.filter,
                    GmosSouthLongSlitFields.fpu,
                    GmosSouthLongSlitFields.central_wavelength().fields(
                        WavelengthFields.nanometers
                    ),
                    GmosSouthLongSlitFields.spatial_offsets().fields(
                        OffsetQFields.arcseconds
                    ),
                ),
                ObservingModeFields.flamingos_2_long_slit().fields(
                    Flamingos2LongSlitFields.decker,
                    Flamingos2LongSlitFields.default_decker,
                    Flamingos2LongSlitFields.default_offsets().fields(
                        OffsetFields.q().fields(
                            OffsetQFields.arcseconds,
                        ),
                        OffsetFields.p().fields(
                            OffsetPFields.arcseconds,
                        ),
                    ),
                    Flamingos2LongSlitFields.disperser,
                    Flamingos2LongSlitFields.filter,
                    Flamingos2LongSlitFields.fpu,
                    Flamingos2LongSlitFields.telluric_type().fields(
                        TelluricTypeFields.tag, TelluricTypeFields.star_types
                    ),
                    Flamingos2LongSlitFields.exposure_time_mode().fields(
                        ExposureTimeModeFields.signal_to_noise().fields(
                            SignalToNoiseExposureTimeModeFields.value,
                            SignalToNoiseExposureTimeModeFields.at().fields(
                                WavelengthFields.nanometers
                            ),
                        ),
                        ExposureTimeModeFields.time_and_count().fields(
                            TimeAndCountExposureTimeModeFields.time().fields(
                                TimeSpanFields.seconds
                            ),
                            TimeAndCountExposureTimeModeFields.count,
                            TimeAndCountExposureTimeModeFields.at().fields(
                                WavelengthFields.nanometers
                            ),
                        ),
                    ),
                    Flamingos2LongSlitFields.explicit_read_mode,
                    Flamingos2LongSlitFields.explicit_reads,
                    Flamingos2LongSlitFields.explicit_decker,
                    Flamingos2LongSlitFields.readout_mode,
                    Flamingos2LongSlitFields.default_readout_mode,
                    Flamingos2LongSlitFields.explicit_read_mode,
                    Flamingos2LongSlitFields.offsets().fields(
                        OffsetFields.q().fields(
                            OffsetQFields.arcseconds,
                        ),
                        OffsetFields.p().fields(
                            OffsetPFields.arcseconds,
                        ),
                    ),
                    Flamingos2LongSlitFields.acquisition().fields(
                        Flamingos2LongSlitAcquisitionFields.exposure_time_mode().fields(
                            ExposureTimeModeFields.signal_to_noise().fields(
                                SignalToNoiseExposureTimeModeFields.value,
                                SignalToNoiseExposureTimeModeFields.at().fields(
                                    WavelengthFields.nanometers
                                ),
                            ),
                            ExposureTimeModeFields.time_and_count().fields(
                                TimeAndCountExposureTimeModeFields.time().fields(
                                    TimeSpanFields.seconds,
                                ),
                                TimeAndCountExposureTimeModeFields.count,
                                TimeAndCountExposureTimeModeFields.at().fields(
                                    WavelengthFields.nanometers
                                ),
                            ),
                        )
                    ),
                    Flamingos2LongSlitFields.initial_disperser,
                    Flamingos2LongSlitFields.initial_filter,
                    Flamingos2LongSlitFields.initial_fpu,
                ),
            ),
            ObservationFields.constraint_set().fields(
                ConstraintSetFields.image_quality,
                ConstraintSetFields.cloud_extinction,
                ConstraintSetFields.sky_background,
                ConstraintSetFields.water_vapor,
                ConstraintSetFields.elevation_range().fields(
                    ElevationRangeFields.air_mass().fields(
                        AirMassRangeFields.min,
                        AirMassRangeFields.max,
                    ),
                    ElevationRangeFields.hour_angle().fields(
                        HourAngleRangeFields.min_hours,
                        HourAngleRangeFields.max_hours,
                    ),
                ),
            ),
            ObservationFields.timing_windows().fields(
                TimingWindowFields.inclusion,
                TimingWindowFields.start_utc,
                TimingWindowFields.end.on(
                    "TimingWindowEndAt", TimingWindowEndAtFields.at_utc
                ),
                TimingWindowFields.end.on(
                    "TimingWindowEndAfter",
                    TimingWindowEndAfterFields.after().fields(TimeSpanFields.seconds),
                    TimingWindowEndAfterFields.repeat().fields(
                        TimingWindowRepeatFields.period().fields(
                            TimeSpanFields.seconds
                        ),
                        TimingWindowRepeatFields.times,
                    ),
                ),
            ),
            ObservationFields.target_environment().fields(
                TargetEnvironmentFields.asterism(include_deleted).fields(
                    TargetFields.sidereal().fields(
                        SiderealFields.ra().fields(RightAscensionFields.hms),
                        SiderealFields.dec().fields(DeclinationFields.dms),
                        SiderealFields.proper_motion().fields(
                            ProperMotionFields.ra().fields(
                                ProperMotionRAFields.milliarcseconds_per_year
                            ),
                            ProperMotionFields.dec().fields(
                                ProperMotionDeclinationFields.milliarcseconds_per_year
                            ),
                        ),
                        SiderealFields.epoch,
                    ),
                    TargetFields.nonsidereal().fields(
                        NonsiderealFields.des,
                    ),
                    TargetFields.name,
                ),
                TargetEnvironmentFields.explicit_base().fields(
                    CoordinatesFields.ra().fields(RightAscensionFields.hms),
                    CoordinatesFields.dec().fields(DeclinationFields.dms),
                ),
            ),
        )
