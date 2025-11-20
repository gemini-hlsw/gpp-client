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
]


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
