"""
Environment definitions for the GPP client.
"""

__all__ = ["GPPEnvironment"]

from enum import Enum

from typing_extensions import Self

from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL


class GPPEnvironment(str, Enum):
    """
    GPP environments with associated metadata.
    """

    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    @property
    def base_url(self) -> str:
        """
        Return the base URL for the environment.

        Returns
        -------
        str
            Base URL for the environment.
        """
        return {
            GPPEnvironment.DEVELOPMENT: DEVELOPMENT_URL,
            GPPEnvironment.PRODUCTION: PRODUCTION_URL,
        }[self]

    @classmethod
    def _missing_(cls, value: object) -> Self | None:
        """
        Handle missing values by matching case-insensitively.
        """
        if not isinstance(value, str):
            return None

        value_normalized = value.strip().upper()
        for member in cls:
            if member.value == value_normalized:
                return member
        return None
