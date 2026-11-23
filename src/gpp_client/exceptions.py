"""
Exceptions for the GPP client library.
"""

__all__ = [
    "GPPError",
    "GPPClientError",
    "GPPAuthError",
    "GPPNetworkError",
    "GPPTimeoutError",
    "GPPResponseError",
    "GPPValidationError",
    "GPPWorkflowTransitionError",
    "GPPRetryableError",
    "WorkflowReason",
]

from dataclasses import dataclass


class GPPError(Exception):
    """
    Base class for all exceptions raised by the GPP client library.
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


@dataclass(frozen=True)
class WorkflowReason:
    """
    One of GPP's reasons about an observation's workflow, word for word.

    Attributes
    ----------
    severity : str
        ``"ERROR"`` when it has to be fixed, ``"WARNING"`` when it only has to be
        reviewed (GPP keeps the observation from ``READY`` until it is dismissed).
    code : str
        GPP's ``ObservationValidationCode``.
    message : str
        GPP's text.
    """

    severity: str
    code: str
    message: str


class GPPWorkflowTransitionError(GPPValidationError):
    """
    Raised when GPP does not allow the requested workflow state.

    Attributes
    ----------
    requested : str
        The state asked for.
    allowed : list[str]
        The states GPP allows from the current one.
    reasons : list[WorkflowReason]
        GPP's reasons, errors before warnings. Empty when GPP gives none.
    """

    def __init__(
        self,
        message: str,
        *,
        requested: str,
        allowed: list[str],
        reasons: list[WorkflowReason],
    ) -> None:
        super().__init__(message)
        self.requested = requested
        self.allowed = allowed
        self.reasons = reasons


class GPPRetryableError(GPPError):
    """
    Raised for errors that may be transient and worth retrying.
    """

    pass


class GPPAuthError(GPPError):
    """
    Raised when authentication fails (missing token, expired token, unauthorized).
    """

    pass


class GPPNetworkError(GPPError):
    """
    Raised when there is a network-related error.
    """

    pass


class GPPTimeoutError(GPPNetworkError):
    """
    Raised when a network operation times out.
    """

    pass


class GPPResponseError(GPPError):
    """
    Raised when GPP returns a non-successful HTTP or GraphQL response.

    This includes:
    - 5xx server errors
    - 4xx errors (if you choose to treat them as exceptional)
    - Valid GraphQL response with an 'errors' field

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
