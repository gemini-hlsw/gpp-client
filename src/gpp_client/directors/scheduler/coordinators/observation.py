from ....coordinator import BaseCoordinator
from ....subscribers import ObservationSubscriber


__all__ = ["ObservationCoordinator"]


class ObservationCoordinator(BaseCoordinator):
    """
    Combines multiple managers and subscribers to return more complex observations.
    """

    async def get_edits(
        self, program_id: str | None = None, observation_id: str | None = None
    ):
        obs_subscriber = ObservationSubscriber(self.client)
        return await obs_subscriber.get_edits(program_id, observation_id)
