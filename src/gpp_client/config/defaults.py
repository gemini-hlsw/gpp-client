"""
Default configuration values for the GPP client.
"""

__all__ = ["GPPDefaults"]

from dataclasses import dataclass, field

from gpp_client.config.environment import GPPEnvironment


@dataclass(frozen=True)
class _GPPDefaults:
    """
    Default values for the GPP client configuration.

    Attributes
    ----------
    config_filename : str
        The name of the configuration file.
    app_name : str
        The name of the application for config directory.
    default_env : GPPEnvironment
        The default GPP environment.
    url : dict[GPPEnvironment, str]
        The default URLs for each GPP environment.
    env_var_env : str
        The environment variable name for the GPP environment.
    env_var_token : str
        The environment variable name for a generic GPP token.
    env_var_env_tokens : dict[GPPEnvironment, str]
        The environment variable names for tokens for each GPP environment.
    disable_env_vars : bool
        The default setting for disabling environment variable usage.
    """

    config_filename: str = "config.toml"
    app_name: str = "gpp-client"
    default_env: GPPEnvironment = GPPEnvironment.PRODUCTION

    url: dict[GPPEnvironment, str] = field(
        default_factory=lambda: {
            GPPEnvironment.DEVELOPMENT: "https://lucuma-postgres-odb-dev.herokuapp.com/odb",
            GPPEnvironment.STAGING: "https://lucuma-postgres-odb-staging.herokuapp.com/odb",
            GPPEnvironment.PRODUCTION: "https://lucuma-postgres-odb-production.herokuapp.com/odb",
        }
    )
    env_var_env: str = "GPP_ENV"
    env_var_token: str = "GPP_TOKEN"
    env_var_env_tokens: dict[GPPEnvironment, str] = field(
        default_factory=lambda: {
            GPPEnvironment.DEVELOPMENT: "GPP_DEVELOPMENT_TOKEN",
            GPPEnvironment.STAGING: "GPP_STAGING_TOKEN",
            GPPEnvironment.PRODUCTION: "GPP_PRODUCTION_TOKEN",
        }
    )
    disable_env_vars: bool = False


GPPDefaults = _GPPDefaults()
