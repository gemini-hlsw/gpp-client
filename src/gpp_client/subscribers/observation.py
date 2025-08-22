from gpp_client.managers.base import BaseManager


__all__ = ["ObservationSubscriber"]


class ObservationSubscriber(BaseManager):
    """
    Allow the access to subscriptions related to observations.

    The subscriptions can be tracked by the id of the observation or the program they belong to.
    """

    async def get_edits(
        self, program_id: str | None = None, observation_id: str | None = None
    ):
        if program_id is None and observation_id is None:
            raise ValueError("Either `program_id` or `observation_id` must be provided")
        if program_id is not None and observation_id is not None:
            raise ValueError("Either `program_id` or `observation_id` must be provided")

        return self.client._client.new_observation_edit(
            program_id=program_id, observation_id=observation_id
        )
