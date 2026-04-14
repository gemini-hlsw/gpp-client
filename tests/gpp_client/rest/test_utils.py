"""
Tests for REST utility helpers.
"""

from pathlib import Path
from types import SimpleNamespace

import pytest

from gpp_client.exceptions import GPPResponseError, GPPValidationError
from gpp_client.rest.utils import raise_for_status, resolve_content


def test_resolve_content_returns_direct_content() -> None:
    """
    Ensure direct content is returned unchanged.
    """
    result = resolve_content(file_path=None, content=b"abc")

    assert result == b"abc"


def test_resolve_content_reads_file_bytes(tmp_path: Path) -> None:
    """
    Ensure file content is read from disk.
    """
    file_path = tmp_path / "data.txt"
    file_path.write_bytes(b"hello")

    result = resolve_content(file_path=file_path, content=None)

    assert result == b"hello"


@pytest.mark.parametrize(
    ("file_path", "content"),
    [
        (None, None),
        ("file.txt", b"abc"),
    ],
)
def test_resolve_content_requires_exactly_one_source(
    file_path: str | None,
    content: bytes | None,
) -> None:
    """
    Ensure exactly one content source is required.
    """
    with pytest.raises(GPPValidationError):
        resolve_content(file_path=file_path, content=content)


def test_resolve_content_raises_for_missing_file(tmp_path: Path) -> None:
    """
    Ensure missing file paths raise validation errors.
    """
    missing_path = tmp_path / "missing.txt"

    with pytest.raises(GPPValidationError):
        resolve_content(file_path=missing_path, content=None)


def test_resolve_content_raises_for_directory(tmp_path: Path) -> None:
    """
    Ensure directory paths raise validation errors.
    """
    with pytest.raises(GPPValidationError):
        resolve_content(file_path=tmp_path, content=None)


@pytest.mark.asyncio
async def test_raise_for_status_allows_ok_status() -> None:
    """
    Ensure accepted statuses do not raise.
    """
    response = SimpleNamespace(
        status=200,
        text=None,
    )

    await raise_for_status(response, ok_statuses={200, 201})


@pytest.mark.asyncio
async def test_raise_for_status_uses_response_text(mocker) -> None:
    """
    Ensure error responses use response text when available.
    """
    response = SimpleNamespace(
        status=500,
        text=mocker.AsyncMock(return_value="Request failed"),
    )

    with pytest.raises(GPPResponseError) as exc_info:
        await raise_for_status(response, ok_statuses={200})

    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "Request failed"
    response.text.assert_awaited_once_with()
