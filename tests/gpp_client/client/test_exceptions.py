"""
Basic coverage tests for GPP exception hierarchy.
"""

import pytest

from gpp_client.exceptions import (
    GPPAuthError,
    GPPClientError,
    GPPError,
    GPPGraphQLError,
    GPPHttpError,
    GPPResponseError,
    GPPRetryableError,
    GPPServerError,
    GPPTransportError,
    GPPValidationError,
    NotAvailable,
)
from gpp_client.generated.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
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
    assert issubclass(NotAvailable, GPPClientError)
    assert issubclass(GPPServerError, GPPError)
    assert issubclass(GPPGraphQLError, GPPServerError)
    assert issubclass(GPPHttpError, GPPServerError)
    assert issubclass(GPPTransportError, GPPServerError)


def test_server_errors_are_still_the_generated_errors_consumers_catch() -> None:
    """
    Test that code catching the generated error classes keeps working.
    """
    assert issubclass(GPPGraphQLError, GraphQLClientGraphQLMultiError)
    assert issubclass(GPPHttpError, GraphQLClientHttpError)
    assert issubclass(GPPTransportError, GraphQLClientError)


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
