from src.gpp_client import GPPClient


class BaseDirector:
    """ Used to orchestrate various managers for a specific service"""
    def __init__(self, client: GPPClient):
        self.client = client