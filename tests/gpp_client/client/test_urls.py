"""
Tests for URL helpers.
"""

import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.urls import get_graphql_url, get_ws_url


@pytest.mark.parametrize(
    ("env", "expected_suffix"),
    [
        (GPPEnvironment.DEVELOPMENT, "/odb"),
        (GPPEnvironment.PRODUCTION, "/odb"),
    ],
)
def test_get_graphql_url(env: GPPEnvironment, expected_suffix: str) -> None:
    """
    Ensure GraphQL URL is constructed correctly.
    """
    url = get_graphql_url(env)
    assert url.endswith(expected_suffix)
    assert url.startswith(env.base_url)


@pytest.mark.parametrize(
    ("env", "expected_scheme"),
    [
        (GPPEnvironment.DEVELOPMENT, "wss"),
        (GPPEnvironment.PRODUCTION, "wss"),
    ],
)
def test_get_ws_url(env: GPPEnvironment, expected_scheme: str) -> None:
    """
    Ensure WebSocket URL is constructed correctly.
    """
    url = get_ws_url(env)

    assert url.startswith(f"{expected_scheme}://")
    assert url.endswith("/ws")
    assert env.base_url.split("://")[1] in url
