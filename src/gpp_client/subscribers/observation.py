from gpp_client.managers.base import BaseManager


__all__ = ["ObservationSubscriber"]


class ObservationSubscriber(BaseManager):
    """
    Allow the access to subscriptions related to observations.

    The subscriptions can be tracked by the id of the observation or the program they belong to.
    """

    async def get_edits(self, program_id: str):
        """
        Bring any edits related to observations inside the program or a specific observation.

        Parameters
        ----------
        program_id : str
            Program id. It would show the edits for all the observations inside the program.

        Returns
        -------
        AsyncIterator[Dict[str, Any]]
            Observation edit changes.
        """

        return self.client.observation_edit(program_id=program_id)

    async def get_calculations_updates(self, program_id: str):
        """
        Bring all the calculations updates related to observations inside the program.

        Parameters
        ----------
        program_id : str, optional
            Program id. It would show the calculations updates for all the observations inside the program.

        Returns
        -------
        AsyncIterator[Dict[str, Any]]
            Observation edit changes.
        """
        return self.client.observation_update_calculations(program_id=program_id)
