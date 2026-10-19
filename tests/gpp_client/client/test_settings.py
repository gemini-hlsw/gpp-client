"""
Tests for GPP settings.
"""

from pydantic import SecretStr

from gpp_client.settings import _unwrap


def test_unwrap_returns_string_value() -> None:
    """
    Ensure SecretStr is unwrapped correctly.
    """
    assert _unwrap(SecretStr("abc")) == "abc"


def test_unwrap_returns_none_for_none() -> None:
    """
    Ensure unwrap returns None when no value is provided.
    """
    assert _unwrap(None) is None
