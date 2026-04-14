"""
Module for base domain functionality and utilities.
"""

__all__ = ["BaseDomain"]

import logging
from pathlib import Path
from typing import NoReturn

from gpp_client.exceptions import (
    GPPClientError,
    GPPError,
    GPPResponseError,
    GPPValidationError,
)
from gpp_client.generated.client import GraphQLClient
from gpp_client.rest.client import RESTClient
from gpp_client.settings import GPPSettings

logger = logging.getLogger(__name__)


class BaseDomain:
    """
    Base class for domain functionality and utilities.

    Parameters
    ----------
    graphql : GraphQLClient
        The GraphQL client instance for making API requests.
    rest : RESTClient
        The REST client instance for making API requests.
    settings : GPPSettings
        The settings instance containing configuration options.
    """

    def __init__(
        self, *, graphql: GraphQLClient, rest: RESTClient, settings: GPPSettings
    ) -> None:
        self._graphql = graphql
        self._rest = rest
        self._settings = settings

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
