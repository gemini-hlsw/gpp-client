from src.directors.scheduler import SchedulerDirector
from src.gpp_client import GPPClient


class Director:
    """Interface to work with different directors."""
    def __init__(self, client: GPPClient):
        # Add here different directors services
        self.scheduler = SchedulerDirector(client)