"""
Utility functions for the GPP client.
"""

from pathlib import Path

from gpp_client.exceptions import (
    GPPClientError,
    GPPResponseError,
    GPPValidationError,
)


def resolve_content(
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
        raise GPPValidationError from exc

    try:
        # Read the file bytes into memory.
        return path.read_bytes()
    except OSError as exc:
        raise GPPClientError from exc


async def raise_for_status(
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
