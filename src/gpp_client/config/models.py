"""
Models for GPP client configuration.
"""

__all__ = ["Tokens", "ConfigFile"]

from pydantic import BaseModel, field_serializer, field_validator

from gpp_client.config.defaults import GPPDefaults
from gpp_client.config.environment import GPPEnvironment


class Tokens(BaseModel):
    """
    Tokens for different GPP environments.
    """

    DEVELOPMENT: str | None = None
    STAGING: str | None = None
    PRODUCTION: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def empty_string_to_none(cls, value):
        """
        Convert empty strings to None.

        Parameters
        ----------
        value : str | None
            The value to validate.

        Returns
        -------
        str | None
            The validated value.
        """
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    @field_serializer("*")
    @classmethod
    def none_to_empty_string(cls, value: str | None) -> str:
        if value is None:
            return ""
        return value


class ConfigFile(BaseModel):
    """
    GPP client configuration file model.
    """

    env: GPPEnvironment = GPPDefaults.default_env
    disable_env_vars: bool = GPPDefaults.disable_env_vars
    tokens: "Tokens" = Tokens()

    @field_serializer("env")
    @classmethod
    def get_enum_value(cls, value: GPPEnvironment) -> str:
        return value.value
