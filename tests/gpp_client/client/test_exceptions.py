"""
Basic coverage tests for GPP exception hierarchy.
"""

import pytest

from gpp_client.environment import GPPEnvironment
from gpp_client.exceptions import (
    GPPAuthError,
    GPPClientError,
    GPPEnvironmentError,
    GPPError,
    GPPResponseError,
    GPPRetryableError,
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


def test_environment_error_says_what_to_change_for_an_unavailable_item():
    error = GPPEnvironmentError(
        "getDraft",
        "operation",
        GPPEnvironment.PRODUCTION,
        [GPPEnvironment.DEVELOPMENT],
    )

    assert error.available == (GPPEnvironment.DEVELOPMENT,)
    assert str(error) == (
        "The operation getDraft is not available on production. It is available "
        "on development. Do not call it on production, or select development "
        'with GPPClient(environment="development") or GPP_ENVIRONMENT=development. '
        "Nothing was sent."
    )


def test_environment_error_says_what_to_change_for_a_required_item():
    error = GPPEnvironmentError(
        "UpdateInput.owner",
        "input field",
        GPPEnvironment.PRODUCTION,
        [GPPEnvironment.DEVELOPMENT],
        required=True,
    )

    assert str(error) == (
        "The input field UpdateInput.owner is required on production. Set it, or "
        "select development, where it is optional, with "
        'GPPClient(environment="development") or GPP_ENVIRONMENT=development. '
        "Nothing was sent."
    )


def test_environment_error_with_no_other_environment_says_only_what_to_change():
    error = GPPEnvironmentError(
        "Kind.NEW", "enum value", GPPEnvironment.DEVELOPMENT, []
    )

    assert str(error) == (
        "The enum value Kind.NEW is not available on development. "
        "Use another value. Nothing was sent."
    )
