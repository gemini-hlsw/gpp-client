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
    "EnvironmentItemKind",
    "GPPEnvironmentError",
    "GPPFieldLeavingWarning",
]

from collections.abc import Iterable
from enum import StrEnum

from gpp_client.environment import GPPEnvironment


class GPPError(Exception):
    """
    Base class for the client's own errors.

    Some calls raise other errors: errors GPP returns for a GraphQL call raise
    the generated ``GraphQLClientError`` subclasses, and some REST and web
    calls raise their HTTP library's errors or ``ValueError``.
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


class EnvironmentItemKind(StrEnum):
    """
    What a ``GPPEnvironmentError`` is about. Each value reads as it does in the
    error message.
    """

    OPERATION = "operation"
    FIELD = "field"
    ARGUMENT = "argument"
    INPUT_FIELD = "input field"
    ENUM_VALUE = "enum value"
    REST_PATH = "REST path"


class GPPEnvironmentError(GPPClientError):
    """
    Raised when a call does not fit the selected environment.

    The call uses an operation, field, argument, input field or enum value the
    environment lacks, or leaves unset an argument or input field it requires.
    A REST path the environment does not serve raises it too, after GPP returns
    404.

    Parameters
    ----------
    item : str
        The operation name, or the schema coordinate of the field
        (``Type.field``), argument (``Type.field(arg:)``), input field
        (``Input.field``) or enum value (``Enum.VALUE``), or the REST path.
    kind : EnvironmentItemKind
        What ``item`` is.
    environment : GPPEnvironment
        The selected environment.
    available : Iterable[GPPEnvironment]
        The environments where the call works as written. When none does, the
        environments that have the item, or, when ``required``, those where it
        may be left unset. Empty for a REST path.
    required : bool, optional
        Whether the environment requires the item and it was not set.
    works_there : bool, optional
        Whether the call as written works on the ``available`` environments.
        When it doesn't, the message doesn't suggest selecting one of them.

    Attributes
    ----------
    item : str
    kind : EnvironmentItemKind
    environment : GPPEnvironment
    available : tuple[GPPEnvironment, ...]
    required : bool
    works_there : bool
    """

    def __init__(
        self,
        item: str,
        kind: EnvironmentItemKind,
        environment: GPPEnvironment,
        available: Iterable[GPPEnvironment],
        *,
        required: bool = False,
        works_there: bool = True,
    ) -> None:
        self.item = item
        self.kind = kind
        self.environment = environment
        self.available = tuple(available)
        self.required = required
        self.works_there = works_there
        super().__init__(self._message())

    def _message(self) -> str:
        selected = self.environment.label
        if self.kind is EnvironmentItemKind.REST_PATH:
            # Nothing tells which environment serves the path, so none is named.
            return (
                f"The REST path {self.item} is not served on {selected}: "
                f"GPP answered 404. Check the path, or wait until {selected} "
                "serves it."
            )
        names = " or ".join(env.label for env in self.available)
        if self.required:
            problem = f"The {self.kind} {self.item} is required on {selected}."
            fix = "Set it"
            where = ", where it is optional,"
        else:
            problem = f"The {self.kind} {self.item} is not available on {selected}." + (
                f" It is available on {names}." if names else ""
            )
            fix = {
                EnvironmentItemKind.OPERATION: "Do not call it",
                EnvironmentItemKind.FIELD: "Do not select it",
                EnvironmentItemKind.ENUM_VALUE: "Use another value",
            }.get(self.kind, "Leave it unset")
            fix = f"{fix} on {selected}" if names else fix
            where = ""
        if not names or not self.works_there:
            return f"{problem} {fix}. Nothing was sent."
        first = self.available[0].label
        return (
            f"{problem} {fix}, or select {first}{where} with "
            f'GPPClient(environment="{first}") or GPP_ENVIRONMENT={first}. '
            "Nothing was sent."
        )


class GPPFieldLeavingWarning(FutureWarning):
    """
    Issued when a call selects a field that development has already removed.

    Changes reach production after development, so expect the field to leave
    production soon. Issued once per field per process.

    Parameters
    ----------
    field : str
        The field's schema coordinate (``Type.field``).
    environment : GPPEnvironment
        The selected environment, which still has the field.

    Attributes
    ----------
    field : str
    environment : GPPEnvironment
    """

    def __init__(self, field: str, environment: GPPEnvironment) -> None:
        self.field = field
        self.environment = environment
        super().__init__(
            f"The field {field} is gone from development and is expected to "
            f"leave {environment.label} at a coming promotion."
        )
