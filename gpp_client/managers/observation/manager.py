from typing import Optional, Any

from gpp_client.managers.base_manager import BaseManager
from gpp_client.mixins import CreateMixin, GetByIdMixin, GetBatchMixin
from . import queries


class ObservationManager(CreateMixin, GetByIdMixin, GetBatchMixin, BaseManager):

    default_fields = queries.DEFAULT_FIELDS

    queries = {
        "get_by_id": queries.GET_OBSERVATION,
        "get_batch": queries.GET_OBSERVATIONS,
    }

    # I'm not quite sure why is this needed and then passed to the methods in the Mixin?
    resource_id_field = "observationId"

    async def get_by_id(
        self,
        *,
        observation_id: str,
        observation_reference: Optional[str] = None,
        fields: Optional[str] = None,
    ) -> dict[str, Any]:

        # Here I'm confused on what the resource_id_field is also a parameter...
        return await super().get_by_id(
            resource_id=observation_id,
            resource_id_field=observation_reference,
            fields=fields,
        )