from gpp_client.managers.base import BaseManager


__all__ = ["TargetSubscriber"]


class TargetSubscriber(BaseManager):
    """
    Allow the access to subscriptions related to Targets.

    The subscriptions can be tracked by the id of the observation or the program they belong to.
    Only program ids are implemented so far.
    """

    async def get_edits(self, program_id: str | None = None):
        """
        Bring any edits related to targets inside the program or a specific observation.

        Parameters
        ----------
        program_id : str
            Program id. It would show the edits for the targets related to this program.

        Returns
        -------
        AsyncIterator[Dict[str, Any]]:
            Observation edit changes.
        """
        return self.client.target_edit(program_id=program_id)
