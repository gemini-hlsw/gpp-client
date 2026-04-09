"""Tests for the attachment domain."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from gpp_client.domains.attachment import (
    AttachmentDomain,
    _build_update_params,
    _build_upload_params,
    _filename_from_presigned_url,
    _remove_headers_middleware,
    _resolve_download_dir,
)
from gpp_client.exceptions import GPPClientError, GPPResponseError
from gpp_client.generated.enums import AttachmentType


@pytest.fixture()
def attachment_domain(domain_kwargs) -> AttachmentDomain:
    """
    Return an attachment domain instance.
    """
    return AttachmentDomain(**domain_kwargs)


class DummyResponseContext:
    """
    Async context manager for a mocked response.
    """

    def __init__(self, response) -> None:
        """
        Store the response object.
        """
        self._response = response

    async def __aenter__(self):
        """
        Return the response.
        """
        return self._response

    async def __aexit__(self, exc_type, exc, tb) -> None:
        """
        Exit the async context manager.
        """
        return None


def test_build_upload_params_includes_required_fields() -> None:
    """
    Ensure upload params include the expected required fields.
    """
    result = _build_upload_params(
        program_id="p-1",
        attachment_type=AttachmentType.FINDER,
        file_name="file.txt",
        description=None,
    )

    assert result == {
        "programId": "p-1",
        "fileName": "file.txt",
        "attachmentType": AttachmentType.FINDER.value,
    }


def test_build_upload_params_strips_description() -> None:
    """
    Ensure upload params strip and include description when present.
    """
    result = _build_upload_params(
        program_id="p-1",
        attachment_type=AttachmentType.FINDER,
        file_name="file.txt",
        description="  hello  ",
    )

    assert result["description"] == "hello"


def test_build_update_params_includes_required_fields() -> None:
    """
    Ensure update params include the required file name.
    """
    assert _build_update_params(file_name="file.txt", description=None) == {
        "fileName": "file.txt"
    }


def test_build_update_params_strips_description() -> None:
    """
    Ensure update params strip and include description when present.
    """
    assert _build_update_params(file_name="file.txt", description="  hi  ") == {
        "fileName": "file.txt",
        "description": "hi",
    }


def test_filename_from_presigned_url_extracts_name() -> None:
    """
    Ensure filename is extracted from presigned URL path.
    """
    result = _filename_from_presigned_url("https://example.test/path/file.txt?x=1")

    assert result == "file.txt"


def test_filename_from_presigned_url_raises_without_name() -> None:
    """
    Ensure filename extraction raises when no filename can be determined.
    """
    with pytest.raises(ValueError):
        _filename_from_presigned_url("https://example.test/")


def test_resolve_download_dir_defaults_to_home(mocker) -> None:
    """
    Ensure resolve_download_dir defaults to the home directory.
    """
    mock_home = Path("/tmp/home")
    mocker.patch("gpp_client.domains.attachment.Path.home", return_value=mock_home)

    assert _resolve_download_dir(None) == mock_home


def test_resolve_download_dir_rejects_file_path(tmp_path: Path) -> None:
    """
    Ensure resolve_download_dir rejects existing files.
    """
    file_path = tmp_path / "file.txt"
    file_path.write_text("x")

    with pytest.raises(ValueError):
        _resolve_download_dir(file_path)


@pytest.mark.asyncio
async def test_remove_headers_middleware_removes_headers(mocker) -> None:
    """
    Ensure presigned URL middleware removes auth and content headers.
    """
    req = SimpleNamespace(
        headers={
            "Authorization": "Bearer token",
            "Content-Type": "text/plain",
            "Other": "keep",
        }
    )
    response = object()

    async def handler(received_req):
        return response

    result = await _remove_headers_middleware(req, handler)

    assert result is response
    assert req.headers == {"Other": "keep"}


@pytest.mark.asyncio
async def test_upload_returns_attachment_id(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure upload returns the created attachment id.
    """
    response = SimpleNamespace(
        status=201,
        text=mocker.AsyncMock(return_value="  att-1  "),
    )
    session = SimpleNamespace(
        post=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    mocker.patch.object(attachment_domain, "resolve_content", return_value=b"data")
    mocker.patch.object(attachment_domain, "raise_for_status", new=mocker.AsyncMock())

    result = await attachment_domain.upload(
        "p-1",
        attachment_type=AttachmentType.FINDER,
        file_name="file.txt",
        content=b"data",
    )

    assert result == "att-1"


@pytest.mark.asyncio
async def test_upload_raises_for_empty_attachment_id(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure upload raises when the returned attachment id is empty.
    """
    response = SimpleNamespace(
        status=201,
        text=mocker.AsyncMock(return_value="   "),
    )
    session = SimpleNamespace(
        post=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    mocker.patch.object(attachment_domain, "resolve_content", return_value=b"data")
    mocker.patch.object(attachment_domain, "raise_for_status", new=mocker.AsyncMock())

    with pytest.raises(GPPClientError):
        await attachment_domain.upload(
            "p-1",
            attachment_type=AttachmentType.FINDER,
            file_name="file.txt",
            content=b"data",
        )


@pytest.mark.asyncio
async def test_upload_reraises_response_error(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure upload re-raises GPPResponseError unchanged.
    """
    response = SimpleNamespace()
    session = SimpleNamespace(
        post=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    mocker.patch.object(attachment_domain, "resolve_content", return_value=b"data")
    mocker.patch.object(
        attachment_domain,
        "raise_for_status",
        new=mocker.AsyncMock(side_effect=GPPResponseError(500, "boom")),
    )

    with pytest.raises(GPPResponseError):
        await attachment_domain.upload(
            "p-1",
            attachment_type=AttachmentType.FINDER,
            file_name="file.txt",
            content=b"data",
        )


@pytest.mark.asyncio
async def test_delete_by_id_dispatches_correctly(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure delete_by_id issues the expected request.
    """
    response = SimpleNamespace(status=204)
    session = SimpleNamespace(
        delete=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    raise_for_status = mocker.patch.object(
        attachment_domain,
        "raise_for_status",
        new=mocker.AsyncMock(),
    )

    await attachment_domain.delete_by_id("att-1")

    session.delete.assert_called_once_with("/attachment/att-1")
    raise_for_status.assert_awaited_once_with(response, ok_statuses={200, 204})


@pytest.mark.asyncio
async def test_update_by_id_dispatches_correctly(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure update_by_id issues the expected request.
    """
    response = SimpleNamespace(status=200)
    session = SimpleNamespace(
        put=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    mocker.patch.object(attachment_domain, "resolve_content", return_value=b"data")
    raise_for_status = mocker.patch.object(
        attachment_domain,
        "raise_for_status",
        new=mocker.AsyncMock(),
    )

    await attachment_domain.update_by_id(
        "att-1",
        file_name="file.txt",
        description="hello",
        content=b"data",
    )

    session.put.assert_called_once()
    raise_for_status.assert_awaited_once_with(response, ok_statuses={200, 201})


@pytest.mark.asyncio
async def test_get_download_url_by_id_returns_text(
    attachment_domain,
    rest,
    mocker,
) -> None:
    """
    Ensure get_download_url_by_id returns the response text.
    """
    response = SimpleNamespace(
        status=200,
        text=mocker.AsyncMock(return_value="https://example.test/file.txt"),
    )
    session = SimpleNamespace(
        get=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)
    mocker.patch.object(attachment_domain, "raise_for_status", new=mocker.AsyncMock())

    result = await attachment_domain.get_download_url_by_id("att-1")

    assert result == "https://example.test/file.txt"


@pytest.mark.asyncio
async def test_download_by_id_downloads_file(
    attachment_domain,
    rest,
    mocker,
    tmp_path: Path,
) -> None:
    """
    Ensure download_by_id downloads chunks to disk.
    """
    download_url = "https://example.test/file.txt"
    mocker.patch.object(
        attachment_domain,
        "get_download_url_by_id",
        new=mocker.AsyncMock(return_value=download_url),
    )
    mocker.patch.object(attachment_domain, "raise_for_status", new=mocker.AsyncMock())

    content = SimpleNamespace()

    async def iter_chunked(chunk_size):
        yield b"hello "
        yield b"world"

    content.iter_chunked = iter_chunked

    response = SimpleNamespace(
        status=200,
        content=content,
    )
    session = SimpleNamespace(
        get=mocker.Mock(return_value=DummyResponseContext(response)),
    )
    rest.get_session = mocker.AsyncMock(return_value=session)

    result = await attachment_domain.download_by_id(
        "att-1",
        save_to=tmp_path,
        overwrite=False,
        chunk_size=4,
    )

    assert result == tmp_path / "file.txt"
    assert result.read_bytes() == b"hello world"


@pytest.mark.asyncio
async def test_download_by_id_rejects_existing_file_without_overwrite(
    attachment_domain,
    rest,
    mocker,
    tmp_path: Path,
) -> None:
    """
    Ensure download_by_id rejects existing files when overwrite is false.
    """
    file_path = tmp_path / "file.txt"
    file_path.write_text("existing")

    rest.get_session = mocker.AsyncMock(return_value=mocker.Mock())
    mocker.patch.object(
        attachment_domain,
        "get_download_url_by_id",
        new=mocker.AsyncMock(return_value="https://example.test/file.txt"),
    )

    with pytest.raises(GPPClientError):
        await attachment_domain.download_by_id(
            "att-1",
            save_to=tmp_path,
            overwrite=False,
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method_name", "graphql_name", "kwargs"),
    [
        (
            "get_all_by_observation_id",
            "get_observation_attachments_by_id",
            {"observation_id": "o-1"},
        ),
        (
            "get_all_by_observation_reference",
            "get_observation_attachments_by_reference",
            {"observation_reference": "obs-ref"},
        ),
        (
            "get_all_by_program_id",
            "get_program_attachments_by_id",
            {"program_id": "p-1"},
        ),
        (
            "get_all_by_program_reference",
            "get_program_attachments_by_program_reference",
            {"program_reference": "prog-ref"},
        ),
        (
            "get_all_by_proposal_reference",
            "get_program_attachments_by_proposal_reference",
            {"proposal_reference": "prop-ref"},
        ),
    ],
)
async def test_attachment_graphql_methods_dispatch_correctly(
    attachment_domain,
    graphql,
    mocker,
    method_name: str,
    graphql_name: str,
    kwargs: dict[str, object],
) -> None:
    """
    Ensure attachment GraphQL methods dispatch correctly.
    """
    result_model = object()
    setattr(graphql, graphql_name, mocker.AsyncMock(return_value=result_model))

    method = getattr(attachment_domain, method_name)
    result = await method(**kwargs)

    assert result is result_model
    getattr(graphql, graphql_name).assert_called_once_with(**kwargs)
