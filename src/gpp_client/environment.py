"""
Environment definitions for the GPP client.

``_DETAILS`` is the one table of environments: everything else that lists them,
from settings to the CLI and the build, derives from it.
"""

__all__ = ["GPPEnvironment"]

from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from typing import Self

from gpp_client.constants import (
    DEVELOPMENT_TOKEN_ENV_VAR,
    DEVELOPMENT_URL,
    PRODUCTION_URL,
    TOKEN_ENV_VAR,
)


@dataclass(frozen=True)
class _Details:
    base_url: str
    token_variable: str


class GPPEnvironment(StrEnum):
    """
    GPP environments, listed in the order GPP changes reach them: development,
    then production.
    """

    DEVELOPMENT = "DEVELOPMENT"
    PRODUCTION = "PRODUCTION"

    @property
    def label(self) -> str:
        """
        Return the name users type and messages show.

        Returns
        -------
        str
            The lowercase name, such as ``"development"``.
        """
        return self.value.lower()

    @property
    def base_url(self) -> str:
        """
        Return the base URL for the environment.

        Returns
        -------
        str
            Base URL for the environment.
        """
        return _DETAILS[self].base_url

    @property
    def token_variable(self) -> str:
        """
        Return the environment variable holding this environment's token.

        Returns
        -------
        str
            The variable name, such as ``"GPP_DEVELOPMENT_TOKEN"``.
        """
        return _DETAILS[self].token_variable

    @classmethod
    def where(
        cls, has: Callable[["GPPEnvironment"], bool]
    ) -> tuple["GPPEnvironment", ...]:
        """
        Return the environments that have something, in promotion order.

        Parameters
        ----------
        has : Callable[[GPPEnvironment], bool]
            Whether an environment has the thing asked about.

        Returns
        -------
        tuple[GPPEnvironment, ...]
            The environments for which ``has`` is true.
        """
        return tuple(env for env in cls if has(env))

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


_DETAILS = {
    GPPEnvironment.DEVELOPMENT: _Details(
        base_url=DEVELOPMENT_URL,
        token_variable=DEVELOPMENT_TOKEN_ENV_VAR,
    ),
    GPPEnvironment.PRODUCTION: _Details(
        base_url=PRODUCTION_URL,
        token_variable=TOKEN_ENV_VAR,
    ),
}
