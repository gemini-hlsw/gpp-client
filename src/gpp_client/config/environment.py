"""
Environment definitions for the GPP client.
"""

__all__ = ["GPPEnvironment"]

from enum import Enum

from typing_extensions import Self


class GPPEnvironment(str, Enum):
    """
    Available GPP environments.
    """

    DEVELOPMENT = "DEVELOPMENT"
    STAGING = "STAGING"
    PRODUCTION = "PRODUCTION"

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        """
        Handle missing values by attempting to match case-insensitively.
        """
        # Only attempt to match if the value is a string.
        if not isinstance(value, str):
            return None

        value_normalized = value.upper()
        for member in cls:
            if member.value == value_normalized:
                return member
        return None
