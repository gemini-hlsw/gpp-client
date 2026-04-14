"""
Tests for constants.
"""

from gpp_client.constants import (
    APP_NAME,
    DEVELOPMENT_TOKEN_ENV_VAR,
    DEVELOPMENT_URL,
    PRODUCTION_URL,
    TOKEN_ENV_VAR,
)


def test_constants_values() -> None:
    """Ensure constants are defined as expected."""
    assert APP_NAME == "gpp-client"
    assert DEVELOPMENT_URL.startswith("https://")
    assert PRODUCTION_URL.startswith("https://")
    assert TOKEN_ENV_VAR == "GPP_TOKEN"
    assert DEVELOPMENT_TOKEN_ENV_VAR == "GPP_DEVELOPMENT_TOKEN"
