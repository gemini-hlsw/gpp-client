__all__ = ["AttachmentManager"]

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import urlparse

from aiohttp import ClientHandlerType, ClientRequest, ClientResponse

from gpp_client.api.custom_fields import (
    AttachmentFields,
    ObservationFields,
    ProgramFields,
)
from gpp_client.api.custom_queries import Query
from gpp_client.exceptions import GPPClientError
from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)
if TYPE_CHECKING:
    from gpp_client.client import GPPClient


class AttachmentManager(BaseManager):
    def __init__(self, client: "GPPClient") -> None:
        super().__init__(client)

        self.rest_client = client._restapi
        self.url = f"{self.rest_client.base_url}/attachment/url"

    async def get_download_url_by_id(self, attachment_id: str) -> str:
        """
        Get the download URL for an attachment by its ID.

        Parameters
        ----------
        attachment_id : str
            The ID of the attachment.

        Returns
        -------
        str
            The download URL for the attachment.
        """
        logger.debug("Getting download URL for attachment %s", attachment_id)
        session = await self.rest_client._get_session()
        url = f"{self.url}/{attachment_id}"

        try:
            async with session.get(url, raise_for_status=True) as response:
                download_url = await response.text()
        except Exception as exc:
            self.raise_error(GPPClientError, exc, include_traceback=True)

        return download_url

    async def download_by_id(
        self,
        attachment_id: str,
        save_to: str | Path | None = None,
        overwrite: bool = False,
        chunk_size: int = 1024 * 1024,
    ) -> None:
        """
        Download an attachment by its ID.

        Parameters
        ----------
        attachment_id : str
            The ID of the attachment.
        save_to : str | Path | None, optional
            The directory to save the downloaded attachment. If ``None``, defaults to home directory.
        overwrite : bool, optional
            Whether to overwrite the file if it already exists. Default is ``False``.
        chunk_size : int, optional
            The chunk size for downloading the file in bytes. Default is 1 MB.
        """
        logger.debug("Downloading attachment %s", attachment_id)
        session = await self.rest_client._get_session()
        download_url = await self.get_download_url_by_id(attachment_id)

        # Get the filename and resolve the destination directory.
        filename = filename_from_presigned_url(download_url)
        dest_dir = resolve_download_dir(save_to)
        logger.debug("Resolved download directory: %s", dest_dir)
        path = dest_dir / filename

        # Create the destination directory if it doesn't exist.
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Check if the file exists and handle overwrite option.
        if path.exists():
            if not overwrite:
                raise GPPClientError(
                    f"File {path} already exists and overwrite is set to False."
                )
            logger.debug("File %s exists, overwriting.", path)
            path.unlink()

        # Use the presigned URL to download the attachment content.
        try:
            async with session.get(
                download_url,
                middlewares=(remove_headers_middleware,),
                raise_for_status=True,
            ) as response:
                # Download the file in chunks to avoid loading it all into memory.
                with path.open("wb") as fh:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        fh.write(chunk)

                logger.info("Downloaded %s", path)

        except Exception as exc:
            self.raise_error(GPPClientError, exc, include_traceback=True)

    async def get_all_by_observation(
        self, *, observation_reference: str | None, observation_id: str | None
    ) -> dict[str, Any]:
        """
        Get all attachments associated with a given observation.

        Parameters
        ----------
        observation_reference : str | None
            The observation reference.
        observation_id : str | None
            The observation ID.

        Returns
        -------
        dict[str, Any]
            A dictionary containing attachment information.
        """
        self.validate_single_identifier(
            observation_id=observation_id, observation_reference=observation_reference
        )

        fields = Query.observation(
            observation_id=observation_id, observation_reference=observation_reference
        ).fields(
            ObservationFields.attachments().fields(*self._fields()),
        )

        operation_name = "observation"
        result = await self.client.query(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    async def get_all_by_program(
        self,
        *,
        program_id: str | None,
        proposal_reference: str | None,
        program_reference: str | None,
    ) -> dict[str, Any]:
        """
        Get all attachments associated with a given program.

        Parameters
        ----------
        program_id : str | None
            The program ID.
        proposal_reference : str | None
            The proposal reference.
        program_reference : str | None
            The program reference.

        Returns
        -------
        dict[str, Any]
            A dictionary containing attachment information.
        """
        self.validate_single_identifier(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        )

        fields = Query.program(
            program_id=program_id,
            program_reference=program_reference,
            proposal_reference=proposal_reference,
        ).fields(
            ProgramFields.attachments().fields(*self._fields()),
        )

        operation_name = "program"
        result = await self.client.query(fields, operation_name=operation_name)

        return self.get_result(result, operation_name)

    @staticmethod
    def _fields() -> tuple:
        """
        Get the fields to retrieve for attachments.

        Returns
        -------
        tuple
            A tuple of attachment field names.
        """
        return (
            AttachmentFields.id,
            AttachmentFields.file_name,
            AttachmentFields.attachment_type,
            AttachmentFields.file_size,
            AttachmentFields.checked,
            AttachmentFields.description,
            AttachmentFields.updated_at,
        )


async def remove_headers_middleware(
    req: ClientRequest,
    handler: ClientHandlerType,
) -> ClientResponse:
    """
    Remove Authorization / Content-Type headers for presigned or external URLs.

    Needed because some presigned URLs (e.g., AWS S3) reject requests with
    unexpected headers.

    Parameters
    ----------
    req : ClientRequest
        The outgoing request.
    handler : ClientHandlerType
        The next handler in the middleware chain.

    Returns
    -------
    ClientResponse
        The response from the handler.
    """
    req.headers.pop("Authorization", None)
    req.headers.pop("Content-Type", None)

    return await handler(req)


def filename_from_presigned_url(download_url: str) -> str:
    """
    Extract filename from a presigned S3 URL.

    Parameters
    ----------
    download_url : str
        The presigned download URL.

    Returns
    -------
    str
        The filename extracted from the URL.
    """
    parsed = urlparse(download_url)
    name = Path(parsed.path).name

    if not name:
        raise ValueError("Could not determine filename from presigned URL")

    return name


def resolve_download_dir(save_to: str | Path | None) -> Path:
    """
    Resolve the download directory.

    Parameters
    ----------
    save_to : str | Path | None
        The directory to save the downloaded file to. If ``None``, defaults to home directory.

    Returns
    -------
    Path
        The resolved directory path.
    """
    # Default is home directory.
    if save_to is None:
        return Path.home()

    path = Path(save_to).expanduser()

    if path.exists() and not path.is_dir():
        raise ValueError(f"save_to must be a directory, got file: {path}")

    return path
