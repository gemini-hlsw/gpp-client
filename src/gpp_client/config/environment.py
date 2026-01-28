"""
Environment definitions for the GPP client.
"""

__all__ = ["GPPEnvironment"]

from enum import Enum


class GPPEnvironment(str, Enum):
    """
    Available GPP environments.

    Attributes
    ----------
    DEVELOPMENT : str
        Development environment.
    STAGING : str
        Staging environment.
    PRODUCTION : str
        Production environment.
    """

    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"
