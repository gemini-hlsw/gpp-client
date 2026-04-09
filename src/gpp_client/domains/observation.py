__all__ = ["ObservationDomain"]

import logging
from collections.abc import AsyncIterator

from gpp_client.domains.base import BaseDomain
from gpp_client.generated.clone_observation import CloneObservation
from gpp_client.generated.create_observation import CreateObservation
from gpp_client.generated.delete_observation_by_id import DeleteObservationById
from gpp_client.generated.delete_observation_by_reference import (
    DeleteObservationByReference,
)
from gpp_client.generated.get_observation import GetObservation
from gpp_client.generated.get_observations import GetObservations
from gpp_client.generated.input_types import (
    CloneObservationInput,
    CreateObservationInput,
    ObservationPropertiesInput,
    UpdateObservationsInput,
    WhereObservation,
)
from gpp_client.generated.obs_calculation_update import ObsCalculationUpdate
from gpp_client.generated.observation_edit import ObservationEdit
from gpp_client.generated.restore_observation_by_id import RestoreObservationById
from gpp_client.generated.restore_observation_by_reference import (
    RestoreObservationByReference,
)
from gpp_client.generated.update_observation_by_id import UpdateObservationById
from gpp_client.generated.update_observation_by_reference import (
    UpdateObservationByReference,
)
from gpp_client.generated.update_observations import UpdateObservations

logger = logging.getLogger(__name__)


class ObservationDomain(BaseDomain):
    async def create(
        self,
        input: CreateObservationInput,
    ) -> CreateObservation:
        """
        Create an observation.

        Parameters
        ----------
        input : CreateObservationInput
            The observation creation input.

        Returns
        -------
        CreateObservation
            The generated GraphQL response model.
        """
        return await self._graphql.create_observation(input=input)

    async def clone(
        self,
        input: CloneObservationInput,
    ) -> CloneObservation:
        """
        Clone an observation.

        Parameters
        ----------
        input : CloneObservationInput
            The clone observation input.

        Returns
        -------
        CloneObservation
            The generated GraphQL response model.
        """
        return await self._graphql.clone_observation(input=input)

    async def update_all(
        self,
        input: UpdateObservationsInput,
    ) -> UpdateObservations:
        """
        Update observations using a bulk update input.

        Parameters
        ----------
        input : UpdateObservationsInput
            The bulk update input.

        Returns
        -------
        UpdateObservations
            The generated GraphQL response model.
        """
        return await self._graphql.update_observations(input=input)

    async def update_by_id(
        self,
        observation_id: str,
        properties: ObservationPropertiesInput,
    ) -> UpdateObservationById:
        """
        Update a single observation by ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.
        properties : ObservationPropertiesInput
            The properties to update.

        Returns
        -------
        UpdateObservationById
            The generated GraphQL response model.
        """
        return await self._graphql.update_observation_by_id(
            observation_id=observation_id,
            set_=properties,
        )

    async def update_by_reference(
        self,
        observation_reference: str,
        properties: ObservationPropertiesInput,
    ) -> UpdateObservationByReference:
        """
        Update a single observation by reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.
        properties : ObservationPropertiesInput
            The properties to update.

        Returns
        -------
        UpdateObservationByReference
            The generated GraphQL response model.
        """
        return await self._graphql.update_observation_by_reference(
            observation_reference=observation_reference,
            set_=properties,
        )

    async def restore_by_id(
        self,
        observation_id: str,
    ) -> RestoreObservationById:
        """
        Restore an observation by ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.

        Returns
        -------
        RestoreObservationById
            The generated GraphQL response model.
        """
        return await self._graphql.restore_observation_by_id(
            observation_id=observation_id
        )

    async def restore_by_reference(
        self,
        observation_reference: str,
    ) -> RestoreObservationByReference:
        """
        Restore an observation by reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.

        Returns
        -------
        RestoreObservationByReference
            The generated GraphQL response model.
        """
        return await self._graphql.restore_observation_by_reference(
            observation_reference=observation_reference
        )

    async def delete_by_id(
        self,
        observation_id: str,
    ) -> DeleteObservationById:
        """
        Delete an observation by ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.

        Returns
        -------
        DeleteObservationById
            The generated GraphQL response model.
        """
        return await self._graphql.delete_observation_by_id(
            observation_id=observation_id
        )

    async def delete_by_reference(
        self,
        observation_reference: str,
    ) -> DeleteObservationByReference:
        """
        Delete an observation by reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.

        Returns
        -------
        DeleteObservationByReference
            The generated GraphQL response model.
        """
        return await self._graphql.delete_observation_by_reference(
            observation_reference=observation_reference
        )

    async def get_by_id(
        self,
        observation_id: str,
    ) -> GetObservation:
        """
        Get an observation by ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.

        Returns
        -------
        GetObservation
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation(observation_id=observation_id)

    async def get_by_reference(
        self,
        observation_reference: str,
    ) -> GetObservation:
        """
        Get an observation by reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.

        Returns
        -------
        GetObservation
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation(
            observation_reference=observation_reference
        )

    async def get_all(
        self,
        *,
        include_deleted: bool,
        where: WhereObservation | None = None,
        offset: str | None = None,
        limit: int | None = None,
    ) -> GetObservations:
        """
        Get observations matching the provided filters.

        Parameters
        ----------
        include_deleted : bool
            Whether to include deleted observations.
        where : WhereObservation | None, optional
            Optional observation filter.
        offset : str | None, optional
            Optional pagination offset.
        limit : int | None, optional
            Optional page size limit.

        Returns
        -------
        GetObservations
            The generated GraphQL response model.
        """
        return await self._graphql.get_observations(
            include_deleted=include_deleted,
            where=where,
            offset=offset,
            limit=limit,
        )

    async def subscribe_to_edits(
        self,
        *,
        program_id: str | None = None,
    ) -> AsyncIterator[ObservationEdit]:
        """
        Subscribe to observation edit events.

        Parameters
        ----------
        program_id : str | None, optional
            Restrict the subscription to a program ID.

        Yields
        ------
        ObservationEdit
            Observation edit events.
        """
        async for event in self._graphql.observation_edit(program_id=program_id):
            yield event

    async def subscribe_to_calculation_updates(
        self,
        *,
        program_id: str | None = None,
    ) -> AsyncIterator[ObsCalculationUpdate]:
        """
        Subscribe to observation calculation update events.

        Parameters
        ----------
        program_id : str | None, optional
            Restrict the subscription to a program ID.

        Yields
        ------
        ObsCalculationUpdate
            Observation calculation update events.
        """
        async for event in self._graphql.obs_calculation_update(program_id=program_id):
            yield event
