__all__ = ["GPPDirector"]

from .client import GPPClient
from .directors import SchedulerDirector


class GPPDirector:
    """
    Interface to access service-specific directors in the GPP client.
    The ``GPPDirector`` class provides higher-level access to composed operations that
    span multiple GraphQL managers. Each attribute corresponds to a domain-specific
    director that encapsulates orchestration logic for that service.

    Parameters
    ----------
    client : GPPClient
        An instance of the `GPPClient` used to communicate with the GPP GraphQL API.

    Attributes
    ----------
    scheduler : SchedulerDirector
        Provides access to scheduler-specific operations, including retrieving programs
        with full observation trees and their live observation metadata.
    """

    def __init__(self, client: GPPClient):
        # Add here different directors services
        self.scheduler = SchedulerDirector(client)
