"""
Basic coverage tests for GPP exception hierarchy.
"""

import pytest

from gpp_client.exceptions import (
    GPPAuthError,
    GPPClientError,
    GPPError,
    GPPNetworkError,
    GPPResponseError,
    GPPRetryableError,
    GPPTimeoutError,
    GPPValidationError,
)


@pytest.mark.parametrize(
    "exc_type",
    [
        GPPError,
        GPPClientError,
        GPPValidationError,
        GPPRetryableError,
        GPPAuthError,
        GPPNetworkError,
        GPPTimeoutError,
    ],
)
def test_exception_can_be_raised(exc_type) -> None:
    """
    Test that each exception type can be raised.
    """
    with pytest.raises(exc_type):
        raise exc_type()


def test_exception_inheritance_tree() -> None:
    """
    Test the exception inheritance hierarchy.
    """
    assert issubclass(GPPClientError, GPPError)
    assert issubclass(GPPValidationError, GPPClientError)
    assert issubclass(GPPRetryableError, GPPError)
    assert issubclass(GPPAuthError, GPPError)
    assert issubclass(GPPNetworkError, GPPError)
    assert issubclass(GPPTimeoutError, GPPNetworkError)


def test_gpp_response_error_fields_and_message() -> None:
    """
    Test that GPPResponseError correctly stores status code and message,
    and that its string representation is as expected.
    """
    exc = GPPResponseError(404, "Not Found")

    assert exc.status_code == 404
    assert exc.message == "Not Found"
    assert str(exc) == "GPP returned 404: Not Found"

    with pytest.raises(GPPResponseError):
        raise exc
