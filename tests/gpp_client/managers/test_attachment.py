from pathlib import Path

import pytest

from gpp_client.api.enums import AttachmentType
from gpp_client.exceptions import GPPClientError, GPPResponseError
from gpp_client.managers.attachment import (
    AttachmentManager,
)


class _AsyncCM:
    """Async context manager wrapper for mocked aiohttp responses."""

    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self._response

    async def __aexit__(self, exc_type, exc, tb):
        return False


class _FakeStream:
    """Fake aiohttp response.content with iter_chunked()."""

    def __init__(self, chunks: list[bytes]) -> None:
        self._chunks = chunks

    async def iter_chunked(self, chunk_size: int):
        for chunk in self._chunks:
            yield chunk


@pytest.fixture
def rest_session(mocker):
    """Mocked aiohttp session returned by rest_client.get_session()."""
    return mocker.MagicMock()


@pytest.fixture
def manager(dummy_client, rest_client, rest_session) -> AttachmentManager:
    rest_client.get_session.return_value = rest_session
    return AttachmentManager(dummy_client)  # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize(
    "description,expected",
    [
        (None, {"programId": "p", "fileName": "f", "attachmentType": "SCIENCE"}),
        ("", {"programId": "p", "fileName": "f", "attachmentType": "SCIENCE"}),
        ("   ", {"programId": "p", "fileName": "f", "attachmentType": "SCIENCE"}),
        (
            "  hello  ",
            {
                "programId": "p",
                "fileName": "f",
                "attachmentType": "SCIENCE",
                "description": "hello",
            },
        ),
    ],
)
def test_build_upload_params_strips_and_optionally_includes_description(
    description: str | None,
    expected: dict[str, str],
) -> None:
    """
    Test that ``_build_upload_params`` correctly handles optional description.
    """
    params = AttachmentManager._build_upload_params(
        program_id="p",
        attachment_type=AttachmentType.SCIENCE,
        file_name="f",
        description=description,
    )
    assert params == expected


@pytest.mark.parametrize(
    "description,expected",
    [
        (None, {"fileName": "f"}),  # Explicit None -> do not send.
        ("", {"fileName": "f"}),  # Empty -> do not send.
        ("   ", {"fileName": "f"}),  # Whitespace -> do not send.
        ("  hello  ", {"fileName": "f", "description": "hello"}),
    ],
)
def test_build_update_params_strips_and_optionally_includes_description(
    description: str | None,
    expected: dict[str, str],
) -> None:
    """
    Test that ``_build_update_params`` correctly handles optional description.
    """
    params = AttachmentManager._build_update_params(
        file_name="f", description=description
    )
    assert params == expected


@pytest.mark.asyncio
async def test_upload_posts_to_attachment_with_params_and_body(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``upload`` calls the correct endpoint with expected params and body.
    """
    manager.resolve_content = mocker.Mock(return_value=b"data")
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 201
    response.text = mocker.AsyncMock(return_value="  att-123  ")
    rest_session.post.return_value = _AsyncCM(response)

    attachment_id = await manager.upload(
        "p1",
        attachment_type=AttachmentType.SCIENCE,
        file_name="file.fits",
        description="  hi  ",
        content=b"ignored-by-mock",
    )

    assert attachment_id == "att-123"

    rest_session.post.assert_called_once()
    _, kwargs = rest_session.post.call_args
    assert kwargs["params"]["programId"] == "p1"
    assert kwargs["params"]["fileName"] == "file.fits"
    assert kwargs["params"]["attachmentType"] == AttachmentType.SCIENCE.value
    assert kwargs["params"]["description"] == "hi"
    assert kwargs["data"] == b"data"

    manager.raise_for_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_upload_raises_if_empty_attachment_id(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``upload`` raises GPPClientError if the response attachment ID is empty.
    """
    manager.resolve_content = mocker.Mock(return_value=b"data")
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 201
    response.text = mocker.AsyncMock(return_value="   ")
    rest_session.post.return_value = _AsyncCM(response)

    with pytest.raises(GPPClientError, match="empty attachment id"):
        await manager.upload(
            "p1",
            attachment_type=AttachmentType.SCIENCE,
            file_name="file.fits",
            content=b"x",
        )


@pytest.mark.asyncio
async def test_upload_propagates_gpp_response_error(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``upload`` propagates GPPResponseError from raise_for_status.
    """
    manager.resolve_content = mocker.Mock(return_value=b"data")
    manager.raise_for_status = mocker.AsyncMock(
        side_effect=GPPResponseError(500, "nope")
    )

    response = mocker.MagicMock()
    response.status = 500
    response.text = mocker.AsyncMock(return_value="nope")
    rest_session.post.return_value = _AsyncCM(response)

    with pytest.raises(GPPResponseError):
        await manager.upload(
            "p1",
            attachment_type=AttachmentType.SCIENCE,
            file_name="file.fits",
            content=b"x",
        )


@pytest.mark.asyncio
async def test_delete_by_id_calls_delete_endpoint_and_checks_status(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``delete_by_id`` calls the correct endpoint and checks the response
    status.
    """
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 204
    rest_session.delete.return_value = _AsyncCM(response)

    await manager.delete_by_id("att-1")

    rest_session.delete.assert_called_once_with("/attachment/att-1")
    manager.raise_for_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_by_id_calls_put_endpoint_with_params_and_body(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``update_by_id`` calls the correct endpoint with expected params and body.
    """
    manager.resolve_content = mocker.Mock(return_value=b"data")
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 200
    rest_session.put.return_value = _AsyncCM(response)

    await manager.update_by_id(
        "att-1",
        file_name="new.txt",
        description="  desc  ",
        content=b"x",
    )

    rest_session.put.assert_called_once()
    _, kwargs = rest_session.put.call_args
    assert kwargs["params"] == {"fileName": "new.txt", "description": "desc"}
    assert kwargs["data"] == b"data"
    manager.raise_for_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_download_url_by_id_calls_url_endpoint_and_returns_text(
    mocker, manager: AttachmentManager, rest_session
) -> None:
    """
    Test that ``get_download_url_by_id`` calls the correct endpoint and returns
    the download URL from the response text.
    """
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 200
    response.text = mocker.AsyncMock(return_value="https://example.com/file")
    rest_session.get.return_value = _AsyncCM(response)

    url = await manager.get_download_url_by_id("att-1")

    assert url == "https://example.com/file"
    rest_session.get.assert_called_once_with(
        "/attachment/url/att-1",
    )
    manager.raise_for_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_download_by_id_streams_to_disk(
    mocker, manager: AttachmentManager, rest_session, tmp_path: Path
) -> None:
    """
    Test that ``download_by_id`` streams the attachment to disk correctly.
    """
    # Pretend presigned URL.
    presigned = "https://host/bucket/myfile.fits?X-Amz-Signature=abc"
    mocker.patch.object(
        manager, "get_download_url_by_id", mocker.AsyncMock(return_value=presigned)
    )
    mocker.patch(
        "gpp_client.managers.attachment.resolve_download_dir", return_value=tmp_path
    )
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    response = mocker.MagicMock()
    response.status = 200
    response.content = _FakeStream([b"a", b"b", b"c"])
    rest_session.get.return_value = _AsyncCM(response)

    path = await manager.download_by_id("att-1", overwrite=False, chunk_size=1)

    assert path == tmp_path / "myfile.fits"
    assert path.read_bytes() == b"abc"

    # Ensure middleware is used for presigned URL call.
    rest_session.get.assert_called_once()
    _, kwargs = rest_session.get.call_args
    assert kwargs["middlewares"] == (mocker.ANY,)  # remove_headers_middleware
    manager.raise_for_status.assert_awaited_once()


@pytest.mark.asyncio
async def test_download_by_id_refuses_to_overwrite_existing_file(
    mocker, manager: AttachmentManager, rest_session, tmp_path: Path
) -> None:
    """
    Test that ``download_by_id`` refuses to overwrite an existing file when
    ``overwrite`` is set to ``False``.
    """
    presigned = "https://host/bucket/myfile.fits?sig=1"
    mocker.patch.object(
        manager, "get_download_url_by_id", mocker.AsyncMock(return_value=presigned)
    )
    mocker.patch(
        "gpp_client.managers.attachment.resolve_download_dir", return_value=tmp_path
    )

    existing = tmp_path / "myfile.fits"
    existing.write_bytes(b"old")

    with pytest.raises(GPPClientError, match="overwrite is set to False"):
        await manager.download_by_id("att-1", overwrite=False)

    rest_session.get.assert_not_called()


@pytest.mark.asyncio
async def test_download_by_id_overwrites_existing_file_when_enabled(
    mocker, manager: AttachmentManager, rest_session, tmp_path: Path
) -> None:
    """
    Test that ``download_by_id`` overwrites an existing file when ``overwrite``
    is set to ``True``.
    """
    presigned = "https://host/bucket/myfile.fits?sig=1"
    mocker.patch.object(
        manager, "get_download_url_by_id", mocker.AsyncMock(return_value=presigned)
    )
    mocker.patch(
        "gpp_client.managers.attachment.resolve_download_dir", return_value=tmp_path
    )
    manager.raise_for_status = mocker.AsyncMock(return_value=None)

    existing = tmp_path / "myfile.fits"
    existing.write_bytes(b"old")

    response = mocker.MagicMock()
    response.status = 200
    response.content = _FakeStream([b"new"])
    rest_session.get.return_value = _AsyncCM(response)

    path = await manager.download_by_id("att-1", overwrite=True)

    assert path.read_bytes() == b"new"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "observation_id,observation_reference,should_raise",
    [
        ("abc", None, False),
        (None, "G-2025A-1234-Q-0001", False),
        (None, None, True),
        ("abc", "G-2025A-1234-Q-0001", True),
    ],
)
async def test_get_all_by_observation_requires_exactly_one_identifier(
    mocker,
    manager: AttachmentManager,
    observation_id,
    observation_reference,
    should_raise,
) -> None:
    """
    Test that ``get_all_by_observation`` requires exactly one identifier.
    """
    if should_raise:
        with pytest.raises(Exception):
            await manager.get_all_by_observation(
                observation_id=observation_id,
                observation_reference=observation_reference,
            )
        return

    # Minimal “happy” response shape.
    manager.client.query.return_value = {"observation": {"attachments": []}}

    result = await manager.get_all_by_observation(
        observation_id=observation_id,
        observation_reference=observation_reference,
    )

    assert "attachments" in result
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == "observation"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "program_id,proposal_reference,program_reference,should_raise",
    [
        ("p1", None, None, False),
        (None, "PR-1", None, False),
        (None, None, "G-2025A-Q-123", False),
        (None, None, None, True),
        ("p1", "PR-1", None, True),
    ],
)
async def test_get_all_by_program_requires_exactly_one_identifier(
    manager: AttachmentManager,
    program_id,
    proposal_reference,
    program_reference,
    should_raise,
) -> None:
    """
    Test that ``get_all_by_program`` requires exactly one identifier.
    """
    if should_raise:
        with pytest.raises(Exception):
            await manager.get_all_by_program(
                program_id=program_id,
                proposal_reference=proposal_reference,
                program_reference=program_reference,
            )
        return

    manager.client.query.return_value = {"program": {"attachments": []}}

    result = await manager.get_all_by_program(
        program_id=program_id,
        proposal_reference=proposal_reference,
        program_reference=program_reference,
    )

    assert "attachments" in result
    _, kwargs = manager.client.query.await_args
    assert kwargs["operation_name"] == "program"
