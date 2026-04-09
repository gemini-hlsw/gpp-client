"""Tests for the base domain."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from gpp_client.domains.base import BaseDomain
from gpp_client.exceptions import (
    GPPClientError,
    GPPResponseError,
    GPPValidationError,
)


class DummyDomain(BaseDomain):
    """Concrete domain for testing BaseDomain behavior."""


@pytest.fixture()
def dummy_domain(domain_kwargs) -> DummyDomain:
    """Return a concrete base domain instance."""
    return DummyDomain(**domain_kwargs)


def test_init_stores_dependencies(dummy_domain, graphql, rest, settings) -> None:
    """Ensure base domain stores shared dependencies."""
    assert dummy_domain._graphql is graphql
    assert dummy_domain._rest is rest
    assert dummy_domain._settings is settings


def test_raise_error_without_traceback(dummy_domain) -> None:
    """Ensure raise_error raises without chaining by default."""
    with pytest.raises(GPPValidationError) as exc_info:
        dummy_domain.raise_error(GPPValidationError, ValueError("bad input"))

    assert str(exc_info.value) == "DummyDomain: bad input"
    assert exc_info.value.__cause__ is None


def test_raise_error_with_traceback(dummy_domain) -> None:
    """Ensure raise_error preserves traceback when requested."""
    original = ValueError("bad input")

    with pytest.raises(GPPValidationError) as exc_info:
        dummy_domain.raise_error(
            GPPValidationError,
            original,
            include_traceback=True,
        )

    assert str(exc_info.value) == "DummyDomain: bad input"
    assert exc_info.value.__cause__ is original


@pytest.mark.asyncio
async def test_raise_for_status_allows_ok_status(dummy_domain, mocker) -> None:
    """Ensure raise_for_status does not raise for allowed statuses."""
    response = SimpleNamespace(
        status=200,
        text=mocker.AsyncMock(),
    )

    await dummy_domain.raise_for_status(response, ok_statuses={200, 201})

    response.text.assert_not_called()


@pytest.mark.asyncio
async def test_raise_for_status_uses_response_text(dummy_domain, mocker) -> None:
    """Ensure raise_for_status uses the response text when available."""
    response = SimpleNamespace(
        status=500,
        text=mocker.AsyncMock(return_value="server exploded"),
    )

    with pytest.raises(GPPResponseError) as exc_info:
        await dummy_domain.raise_for_status(response, ok_statuses={200})

    assert exc_info.value.status_code == 500
    assert exc_info.value.message == "server exploded"


def test_resolve_content_returns_direct_content(dummy_domain) -> None:
    """Ensure direct content is returned unchanged."""
    result = dummy_domain.resolve_content(file_path=None, content=b"abc")

    assert result == b"abc"


@pytest.mark.parametrize(
    ("file_path", "content"),
    [
        (None, None),
        ("file.txt", b"abc"),
    ],
)
def test_resolve_content_requires_exactly_one_source(
    dummy_domain,
    file_path: str | None,
    content: bytes | None,
) -> None:
    """Ensure exactly one content source is required."""
    with pytest.raises(GPPValidationError):
        dummy_domain.resolve_content(file_path=file_path, content=content)


def test_resolve_content_reads_file_bytes(dummy_domain, tmp_path: Path) -> None:
    """Ensure file content is read from disk."""
    file_path = tmp_path / "data.txt"
    file_path.write_bytes(b"hello")

    result = dummy_domain.resolve_content(file_path=file_path, content=None)

    assert result == b"hello"


def test_resolve_content_raises_client_error_on_os_error(
    dummy_domain,
    mocker,
    tmp_path: Path,
) -> None:
    """Ensure file read OS errors are wrapped as client errors."""
    file_path = tmp_path / "data.txt"
    file_path.write_bytes(b"hello")

    mocker.patch.object(Path, "read_bytes", side_effect=OSError("boom"))

    with pytest.raises(GPPClientError):
        dummy_domain.resolve_content(file_path=file_path, content=None)
