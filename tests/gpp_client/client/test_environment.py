"""
Tests for environment definitions.
"""

import pytest

from gpp_client.constants import DEVELOPMENT_URL, PRODUCTION_URL
from gpp_client.environment import GPPEnvironment
from gpp_client.settings import GPPSettings


@pytest.mark.parametrize(
    ("env", "expected_url"),
    [
        (GPPEnvironment.DEVELOPMENT, DEVELOPMENT_URL),
        (GPPEnvironment.PRODUCTION, PRODUCTION_URL),
    ],
)
def test_environment_base_url(env: GPPEnvironment, expected_url: str) -> None:
    """
    Ensure environment base_url resolves correctly.
    """
    assert env.base_url == expected_url


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("development", GPPEnvironment.DEVELOPMENT),
        ("DEVELOPMENT", GPPEnvironment.DEVELOPMENT),
        (" production ", GPPEnvironment.PRODUCTION),
    ],
)
def test_environment_missing_case_insensitive(
    value: str,
    expected: GPPEnvironment,
) -> None:
    """
    Ensure environment parsing is case-insensitive.
    """
    assert GPPEnvironment(value) is expected


def test_environment_missing_invalid_returns_none() -> None:
    """
    Ensure invalid environment values raise ValueError.
    """
    with pytest.raises(ValueError):
        GPPEnvironment("invalid")


def test_environments_are_development_then_production() -> None:
    assert tuple(GPPEnvironment) == (
        GPPEnvironment.DEVELOPMENT,
        GPPEnvironment.PRODUCTION,
    )


@pytest.mark.parametrize("env", list(GPPEnvironment))
def test_every_environment_has_a_token_setting(env: GPPEnvironment) -> None:
    assert GPPSettings(environment=env).with_token("t").resolved_token == "t"
