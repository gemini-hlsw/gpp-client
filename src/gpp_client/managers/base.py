"""
Base class for all resource managers.
"""

__all__ = ["BaseManager"]

import json
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any, NoReturn, Optional, TypeVar

from pydantic import BaseModel, ValidationError

from gpp_client.exceptions import (
    GPPClientError,
    GPPError,
    GPPResponseError,
    GPPValidationError,
)

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from gpp_client.client import GPPClient

T = TypeVar("T", bound=BaseModel)


class BaseManager:
    """
    Base class for all resource managers.

    Provides access to the underlying GraphQL client used to perform operations.

    Parameters
    ----------
    client : GPPClient
        The public-facing client instance. This is used to extract the internal
        GraphQL client used for executing queries and mutations.
    """

    def __init__(self, client: "GPPClient") -> None:
        self.client = client._client
        self.rest_client = client._rest_client

    def raise_error(
        self,
        exc_class: type[GPPError],
        exc: Exception,
        *,
        include_traceback: bool = False,
    ) -> NoReturn:
        """
        Raise a structured exception with contextual information.

        Parameters
        ----------
        exc_class : type[GPPError]
            The exception class to raise (must accept a string message).
        exc : Exception
            The original exception to wrap.
        include_traceback : bool, default=False
            Whether to include the original traceback using `from exc`.

        Raises
        ------
        type[GPPError]
            The raised exception of the specified type.
        """
        class_name = self.__class__.__name__
        message = f"{class_name}: {exc}"
        logger.error(message, exc_info=include_traceback)

        if include_traceback:
            raise exc_class(message) from exc
        raise exc_class(message) from None

    async def raise_for_status(
        self,
        response,
        *,
        ok_statuses: set[int],
        default_message: str = "Request failed",
    ) -> None:
        """
        Raise an exception if the HTTP response status is not OK.

        Parameters
        ----------
        response : aiohttp.ClientResponse
            The HTTP response to check.
        ok_statuses : set[int]
            Set of acceptable HTTP status codes.
        default_message : str, default="Request failed"
            Default error message if the response has no content.

        Raises
        ------
        GPPResponseError
            If the response status is not in ``ok_statuses``.
        """
        if response.status not in ok_statuses:
            text = await response.text()
            raise GPPResponseError(response.status, text or default_message)

    def get_single_result(
        self,
        payload: dict[str, Any],
        key: str,
    ) -> dict[str, Any]:
        """
        Extract exactly one item from a list-valued field in a GraphQL payload.

        Parameters
        ----------
        payload : dict[str, Any]
            The GraphQL payload containing the field.
        key : str
            The key of the field to extract.

        Returns
        -------
        dict[str, Any]
            The single item extracted from the field.

        Raises
        ------
        GPPClientError
            If the specified field is missing from the payload, is not a list,
            or does not contain exactly one item.
        """
        try:
            return self._get_single_result(payload, key)
        except (KeyError, TypeError, ValueError) as exc:
            self.raise_error(GPPClientError, exc)

    def get_result(
        self,
        result: dict[str, Any] | None,
        operation_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Extract the payload for a given GraphQL operation.

        Parameters
        ----------
        result : dict[str, Any] | None
            The full GraphQL result.
        operation_name : str | None, optional
            The name of the operation to extract. If ``None``, and the result
            contains exactly one top-level key, that key is used.

        Returns
        -------
        dict[str, Any]
            The extracted payload for the specified operation.

        Raises
        ------
        GPPClientError
            If the result is empty or invalid, or if the specified operation
            name is not found in the result.
        """
        try:
            return self._get_result(result, operation_name)
        except (ValueError, KeyError) as exc:
            self.raise_error(GPPClientError, exc)

    def resolve_content(
        self,
        *,
        file_path: str | Path | None,
        content: bytes | None,
    ) -> bytes:
        """
        Resolve upload content bytes from exactly one source.

        Parameters
        ----------
        file_path : str | Path | None
            Path to a local file. If provided, it must exist and be a file.
        content : bytes | None
            Raw bytes content.

        Returns
        -------
        bytes
            The resolved content bytes.

        Raises
        ------
        GPPValidationError
            If both or neither of ``file_path`` and ``content`` are provided, or if
            ``file_path`` is invalid.
        GPPClientError
            If reading the file fails due to an unexpected I/O error.
        """
        try:
            has_file_path = file_path is not None
            has_content = content is not None

            # Validate exactly one source is provided.
            if has_file_path == has_content:
                raise ValueError(
                    "Provide exactly one of 'file_path' or 'content', but not both."
                )

            if content is not None:
                return content

            path = Path(file_path).expanduser()  # type: ignore[arg-type]

            # Validate the file exists and is a file.
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            if not path.is_file():
                raise ValueError(f"Expected a file path, got: {path}")

        except (ValueError, FileNotFoundError, TypeError) as exc:
            self.raise_error(GPPValidationError, exc)

        try:
            # Read the file bytes into memory.
            return path.read_bytes()
        except OSError as exc:
            self.raise_error(GPPClientError, exc)

    def validate_single_identifier(self, **kwargs) -> None:
        """
        Validate that exactly one identifier is provided.

        This helper checks that exactly one of the provided keyword arguments
        is non-None. It raises a ValueError otherwise.

        Parameters
        ----------
        **kwargs : dict[str, Optional[str]]
            A dictionary of identifier keyword arguments to validate.

        Raises
        ------
        GPPValidationError
            If none or more than one identifiers are provided.
        """
        try:
            non_null = [k for k, v in kwargs.items() if v is not None]
            if len(non_null) != 1:
                raise ValueError(
                    f"Expected exactly one of {', '.join(kwargs.keys())}, got {len(non_null)}."
                )
        except ValueError as exc:
            self.raise_error(GPPValidationError, exc)

    def load_properties(
        self,
        *,
        properties: Optional[Any],
        from_json: Optional[str | Path | dict[str, Any]],
        cls: type[T],
    ) -> T:
        """
        Return a validated properties object from exactly one data source.

        Parameters
        ----------
        properties : T, optional
            Preconstructed properties instance. Returned unchanged when provided.
        from_json : str | Path | dict[str, Any], optional
            Path to a JSON file or a dictionary containing the JSON data.
        cls : type[T]
            Concrete PropertiesInput class for validation. Required.

        Returns
        -------
        T
            Instance of ``cls`` representing the validated properties.

        Raises
        ------
        GPPValidationError
            If validation fails or an error occurs loading the properties.
        """
        try:
            return self._load_properties(
                properties=properties, from_json=from_json, cls=cls
            )
        except (
            ValueError,
            FileNotFoundError,
            TypeError,
            json.JSONDecodeError,
            ValidationError,
        ) as exc:
            self.raise_error(GPPValidationError, exc)

    def _load_properties(
        self,
        *,
        properties: Optional[T] = None,
        from_json: Optional[str | Path | dict[str, Any]] = None,
        cls: type[T],
    ) -> T:
        """
        Return a validated properties object from exactly one data source.

        Parameters
        ----------
        properties : T, optional
            Preconstructed properties instance. Returned unchanged when provided.
        from_json : str | Path | dict[str, Any], optional
            Path to a JSON file or a dictionary containing the JSON data.
        cls : Type[T]
            Concrete PropertiesInput class for validation. Required.

        Returns
        -------
        T
            Instance of ``cls`` representing the validated properties.

        Raises
        ------
        ValueError
            Raised when both or neither of ``properties`` and ``from_json`` are provided.
        FileNotFoundError
            Raised when ``from_json`` is a path that does not exist.
        json.JSONDecodeError
            Raised when the JSON file cannot be parsed.
        TypeError
            Raised when ``from_json`` is neither path-like nor a mapping.
        ValidationError
            Raised when the loaded data fails validation against ``cls``.
        """
        # Ensure exactly one data source is provided.
        if (properties is None) == (from_json is None):
            raise ValueError(
                "Provide exactly one of 'properties' or 'from_json', but not both."
            )

        if properties is not None:
            return properties

        # Load data from dictionary or JSON file.
        if isinstance(from_json, dict):
            data = from_json
        else:
            path = Path(from_json).expanduser()
            if not path.is_file():
                raise FileNotFoundError(f"JSON properties file not found: {path}")
            with path.open() as f:
                data = json.load(f)

        return cls(**data)

    def _get_result(
        self,
        result: dict[str, Any] | None,
        operation_name: str | None = None,
    ) -> dict[str, Any]:
        """
        Extract the payload for a given GraphQL operation.

        Parameters
        ----------
        result : dict[str, Any] | None
            The full GraphQL result.
        operation_name : str | None, optional
            The name of the operation to extract. If ``None``, and the result
            contains exactly one top-level key, that key is used.

        Returns
        -------
        dict[str, Any]
            The extracted payload for the specified operation.

        Raises
        ------
        ValueError
            If the result is empty or invalid.
        KeyError
            If the specified operation name is not found in the result.
        """
        if result is None or not isinstance(result, dict) or not result:
            raise ValueError("GraphQL response payload is empty or not a dictionary.")

        if operation_name is None:
            if len(result) == 1:
                operation_name = next(iter(result))
            else:
                raise KeyError(
                    "No operation name provided and multiple keys present in "
                    f"result: {list(result)}"
                )

        try:
            return result[operation_name]
        except KeyError:
            raise KeyError(
                f"Expected operation '{operation_name}' not found in result. "
                f"Available keys: {list(result)}"
            )

    def _get_single_result(
        self,
        payload: dict[str, Any],
        key: str,
    ) -> dict[str, Any]:
        """
        Extract exactly one item from a list-valued field in a GraphQL payload.

        Parameters
        ----------
        payload : dict[str, Any]
            The GraphQL payload containing the field.
        key : str
            The key of the field to extract.

        Returns
        -------
        dict[str, Any]
            The single item extracted from the field.

        Raises
        ------
        KeyError
            If the specified field is missing from the payload.
        TypeError
            If the specified field is not a list.
        ValueError
            If the list does not contain exactly one item.
        """
        try:
            # Extract the list from the payload.
            items = payload[key]
        except (KeyError, TypeError):
            raise KeyError(f"Missing expected key '{key}' in GraphQL payload.")

        # Validate the field is a list.
        if not isinstance(items, list):
            raise TypeError(
                f"Expected field '{key}' to be a list, got {type(items).__name__}."
            )
        # Validate the list contains exactly one item.
        if len(items) != 1:
            raise ValueError(
                f"Field '{key}' must contain exactly one item, got {len(items)}."
            )

        return items[0]
