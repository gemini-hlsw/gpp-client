from gpp_client.client import GPPClient
from gpp_client.director import GPPDirector

__all__ = ["GPPClient", "GPPDirector"]

import logging

logger = logging.getLogger(__name__)
# Attach a null handler by default to avoid "No handler found" warnings.
logger.addHandler(logging.NullHandler())
