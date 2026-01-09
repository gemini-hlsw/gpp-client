"""
Environment definitions for the GPP client.
"""

__all__ = ["GPPEnvironment"]

from enum import Enum


class GPPEnvironment(str, Enum):
    """
    Available GPP environments.
    """

    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
