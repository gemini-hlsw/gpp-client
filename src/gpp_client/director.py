"""
Module providing the ``GPPDirector`` class for high-level access to service-specific directors.
"""

__all__ = ["GPPDirector"]

import logging

from gpp_client.client import GPPClient
from gpp_client.directors import GOATSDirector, SchedulerDirector

logger = logging.getLogger(__name__)


class GPPDirector:
    """
    Interface to access service-specific directors in the GPP client.
    The ``GPPDirector`` class provides higher-level access to composed operations that
    span multiple GraphQL managers. Each attribute corresponds to a domain-specific
    director that encapsulates orchestration logic for that service.

    Parameters
    ----------
    client : GPPClient
        Pre-configured client used to perform raw GraphQL operations.

    Attributes
    ----------
    scheduler : SchedulerDirector
        High-level director for Scheduler-domain workflows.
    goats : GOATSDirector
        High-level director for GOATS-domain workflows.
    """

    def __init__(self, client: GPPClient):
        logger.debug("Initializing GPPDirector")
        self._init_directors(client)

    def _init_directors(self, client: GPPClient):
        """
        Initialize all service-specific directors with the provided client.
        """
        self.scheduler = SchedulerDirector(client)
        self.goats = GOATSDirector(client)
