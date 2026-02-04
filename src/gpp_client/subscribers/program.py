from gpp_client.managers.base import BaseManager


__all__ = ["ProgramSubscriber"]


class ProgramSubscriber(BaseManager):
    """
    Allow the access to subscriptions related to Programs.

    The subscriptions can be tracked by the id of the observation or the program they belong to.
    """

    async def get_edits(self, program_id: str | None = None):
        """
        Bring any edits related to a given program.

        Parameters
        ----------
        program_id : str, optional
            Program id. It would show the edits in the program structure.

        Returns
        -------
        AsyncIterator[Dict[str, Any]]
            AsyncProgram edit changes.
        """
        return self.client.program_edit(program_id=program_id)
