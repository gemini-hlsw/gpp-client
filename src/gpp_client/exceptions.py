"""
Exceptions for the GPP client library.
"""

__all__ = [
    "GPPError",
    "GPPClientError",
    "GPPAuthError",
    "GPPResponseError",
    "GPPValidationError",
    "GPPRetryableError",
    "GPPServerError",
    "GPPGraphQLError",
    "GPPHttpError",
    "GPPTransportError",
    "NotAvailable",
]

from collections.abc import Iterable
from typing import Any

from gpp_client.bundled_schemas import bundled_schema
from gpp_client.environment import GPPEnvironment
from gpp_client.generated.exceptions import (
    GraphQLClientError,
    GraphQLClientGraphQLError,
    GraphQLClientGraphQLMultiError,
    GraphQLClientHttpError,
)


class GPPError(Exception):
    """
    Base class for every error the client raises.
    """

    pass


class GPPClientError(GPPError):
    """
    Raised when there is a client-side error.
    """

    pass


class GPPValidationError(GPPClientError):
    """
    Raised when there is a validation error (e.g., invalid input data).
    """

    pass


class GPPRetryableError(GPPError):
    """
    Raised for errors that may be transient and worth retrying.
    """

    pass


class GPPAuthError(GPPError):
    """
    Raised when the selected environment has no token.
    """

    pass


class GPPResponseError(GPPError):
    """
    Raised when GPP refuses an attachment upload, download, update or delete.

    Parameters
    ----------
    status_code : int
        The HTTP status code returned by GPP.
    message : str
        The error message or description.
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"GPP returned {status_code}: {message}")


class NotAvailable(GPPClientError):  # noqa: N818
    """
    Raised when the selected environment lacks what a call needs.

    A generated operation the environment lacks raises it before anything is
    sent; a REST path the environment does not serve raises it after GPP
    answers 404.

    Parameters
    ----------
    item : str
        The operation name, or the REST path.
    kind : str
        What ``item`` is, as the message reads it: ``"operation"`` or
        ``"REST path"``.
    environment : GPPEnvironment
        The selected environment.
    available : Iterable[GPPEnvironment], optional
        The environments that have the item, when known.
    then : str, optional
        The message's last sentence, saying what happened.

    Attributes
    ----------
    item : str
    kind : str
    environment : GPPEnvironment
    available : tuple[GPPEnvironment, ...]
    """

    def __init__(
        self,
        item: str,
        kind: str,
        environment: GPPEnvironment,
        available: Iterable[GPPEnvironment] = (),
        then: str = "Nothing was sent.",
    ) -> None:
        self.item = item
        self.kind = kind
        self.environment = environment
        self.available = tuple(available)
        message = f"The {kind} {item} is not available on {environment.label}."
        if self.available:
            names = " or ".join(env.label for env in self.available)
            message += f" It is available on {names}."
        super().__init__(f"{message} {then}")


class GPPServerError(GPPError):
    """
    Raised when GPP answers a request with an error, or cannot be reached.

    The message names the environment and the schema the client was built
    from, so an install that is behind the server reads differently from
    wrong data or the wrong environment.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment the request went to.
    what : str
        What went wrong, following the environment's name in the message,
        such as ``"returned errors"``.
    detail : str, optional
        What GPP said, after a colon at the end of the message.

    Attributes
    ----------
    environment : GPPEnvironment
    schema : BundledSchema
        The environment's schema as the client was built from it.
    """

    def __init__(
        self, environment: GPPEnvironment, what: str, detail: str = ""
    ) -> None:
        self.environment = environment
        self.schema = bundled_schema(environment)
        message = (
            f"GPP {environment.label} {what} (the client was built from {self.schema})"
        )
        Exception.__init__(self, f"{message}: {detail}" if detail else message)

    def __str__(self) -> str:
        return self.args[0]


class GPPGraphQLError(GPPServerError, GraphQLClientGraphQLMultiError):
    """
    Raised when GPP returns GraphQL errors for a call or a subscription.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment that answered.
    errors : list[GraphQLClientGraphQLError]
        The errors GPP returned.
    data : dict[str, Any] | None, optional
        The ``data`` GPP returned next to the errors, for a partial response.

    Attributes
    ----------
    errors : list[GraphQLClientGraphQLError]
    data : dict[str, Any] | None
    """

    def __init__(
        self,
        environment: GPPEnvironment,
        errors: list[GraphQLClientGraphQLError],
        data: dict[str, Any] | None = None,
    ) -> None:
        self.errors = errors
        self.data = data
        super().__init__(
            environment,
            "returned errors",
            "; ".join(error.message for error in errors),
        )


class GPPHttpError(GPPServerError, GraphQLClientHttpError):
    """
    Raised when GPP answers a request with an HTTP error status.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment that answered.
    status_code : int
        The HTTP status.
    response : Any
        The HTTP response, as the HTTP library returned it.
    detail : str, optional
        The response body, when it says why.

    Attributes
    ----------
    status_code : int
    response : Any
    """

    def __init__(
        self,
        environment: GPPEnvironment,
        status_code: int,
        response: Any,
        detail: str = "",
    ) -> None:
        self.status_code = status_code
        self.response = response
        super().__init__(environment, f"answered HTTP {status_code}", detail)


class GPPTransportError(GPPServerError, GraphQLClientError):
    """
    Raised when GPP cannot be reached, or answers with something that is not
    GraphQL.

    A connection failure, a timeout, a dropped websocket, a response that is
    not JSON, or a websocket message the client cannot read all raise it.
    ``__cause__`` holds the HTTP or websocket library's own error.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment the request went to.
    what : str
        What went wrong, following the environment's name in the message.
    detail : str, optional
        The library's own message.
    """

    def __init__(
        self, environment: GPPEnvironment, what: str, detail: str = ""
    ) -> None:
        super().__init__(environment, what, detail)
