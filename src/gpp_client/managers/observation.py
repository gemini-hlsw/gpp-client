__all__ = ["ObservationManager"]

from pathlib import Path
from typing import Any, Optional

from ..api.custom_fields import (
    CreateObservationResultFields,
    ObservationFields,
    ObservationReferenceFields,
    ObservationSelectResultFields,
    ProgramFields,
    ScienceRequirementsFields,
    UpdateObservationsResultFields,
    TimeSpanFields,
    ConstraintSetFields,
    TimingWindowFields,
    TimingWindowEndAtFields,
    TimingWindowEndAfterFields,
    TimingWindowRepeatFields,
    ElevationRangeFields,
    AirMassRangeFields,
    HourAngleRangeFields,
    TargetEnvironmentFields,
    CoordinatesFields,
    RightAscensionFields,
    DeclinationFields,
    TargetFields,
    SiderealFields,
    ProperMotionFields,
    ProperMotionRAFields,
    ProperMotionDeclinationFields,
    NonsiderealFields,
    CalculatedObservationWorkflowFields,
)
from ..api.custom_mutations import Mutation
from ..api.custom_queries import Query
from ..api.enums import Existence
from ..api.input_types import (
    CreateObservationInput,
    ObservationPropertiesInput,
    UpdateObservationsInput,
    WhereObservation,
    WhereObservationReference,
    WhereOrderObservationId,
    WhereString,
)
from .base import BaseManager
from .utils import load_properties, validate_single_identifier


class ObservationManager(BaseManager):
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
        ValueError
            - If no valid program identifier is provided.
            - If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        validate_single_identifier(
            program_id=program_id,
            proposal_reference=proposal_reference,
            program_reference=program_reference,
        )

        properties = load_properties(
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

        return result[operation_name]

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
        ValueError
            If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        properties = load_properties(
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

        return result[operation_name]

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
        ValueError
            - If neither or both of `observation_id` and `observation_reference` are
            provided.
            - If zero or both of ``properties`` and ``from_json`` are provided.

        Notes
        -----
        Exactly one of ``properties`` or ``from_json`` must be supplied. Supplying
        both or neither raises ``ValueError``.
        """
        validate_single_identifier(
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

        return result["observations"][0]

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
        ValueError
            If neither or both of `observation_id` and `observation_reference` are
            provided.
        """
        validate_single_identifier(
            observation_id=observation_id, observation_reference=observation_reference
        )

        fields = Query.observation(
            observation_id=observation_id, observation_reference=observation_reference
        ).fields(*self._fields(include_deleted=include_deleted))

        operation_name = "observation"
        result = await self.client.query(fields, operation_name=operation_name)

        return result[operation_name]

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
        """
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

        return result[operation_name]

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
        ValueError
            If neither or both of `observation_id` and `observation_reference` are provided.
        """
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
        ValueError
            If neither or both of `observation_id` and `observation_reference` are provided.
        """
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
            ObservationFields.calculated_workflow().fields(
                CalculatedObservationWorkflowFields.state
            ),
            # BEGIN SEQUENCE NEEDED
            # ObservationFields.execution().fields(
            # DEPRECATED, use calculated_digest
            #    ExecutionFields.digest().fields(
            #        ExecutionDigestFields.setup().fields(
            #            SetupTimeFields.full().fields(
            #                TimeSpanFields.seconds
            #            ),
            #            SetupTimeFields.reacquisition().fields(
            #                TimeSpanFields.seconds
            #            )
            #        )
            #    )
            # ),
            # END SEQUENCE
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
