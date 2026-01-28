__all__ = ["AttachmentManager"]

import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from aiohttp import ClientHandlerType, ClientRequest, ClientResponse

from gpp_client.api.custom_fields import (
    AttachmentFields,
    ObservationFields,
    ProgramFields,
)
from gpp_client.api.custom_queries import Query
from gpp_client.api.enums import AttachmentType
from gpp_client.exceptions import GPPClientError
from gpp_client.managers.base import BaseManager

logger = logging.getLogger(__name__)


class AttachmentManager(BaseManager):
    async def upload(
        self,
        program_id: str,
        *,
        attachment_type: AttachmentType,
        file_name: str,
        description: str | None = None,
        file_path: str | Path | None = None,
        content: bytes | None = None,
    ) -> str:
        """
        Upload a new attachment for a program.

        Parameters
        ----------
        program_id : str
            The program ID to associate the attachment with.
        attachment_type : AttachmentType
            The attachment type.
        file_name : str
            The file name to store for the attachment.
        description : str | None, optional
            Optional attachment description.
        file_path : str | Path | None, optional
            Path to a file whose contents will be uploaded. Mutually exclusive with ``content``.
        content : bytes | None, optional
            Raw bytes to upload. Mutually exclusive with ``file_path``.

        Returns
        -------
        str
            The created attachment ID.

        Raises
        ------
        GPPClientError
            If the upload fails or the response is invalid.
        GPPValidationError
            If a validation error occurs.
        """
        logger.debug(
            "Uploading attachment for program %s (type=%s, file_name=%s)",
            program_id,
            attachment_type,
            file_name,
        )

        body = self.resolve_content(file_path=file_path, content=content)

        params: dict[str, str] = {
            "programId": program_id,
            "fileName": file_name,
            "attachmentType": attachment_type.value,
        }
        if description and description.strip():
            params["description"] = description.strip()

        session = await self.rest_client._get_session()
        url = "/attachment"

        try:
            async with session.post(url, params=params, data=body) as response:
                text = await response.text()

                if response.status not in {200, 201}:
                    raise GPPClientError(
                        "Failed to upload attachment "
                        f"(status={response.status}): {text}"
                    )

                attachment_id = text.strip()
                if not attachment_id:
                    raise GPPClientError(
                        "Upload attachment returned an empty attachment id."
                    )

                logger.debug("Uploaded attachment id=%s", attachment_id)
                return attachment_id

        except Exception as exc:
            self.raise_error(GPPClientError, exc)

    async def delete_by_id(self, attachment_id: str) -> None:
        """
        Delete an attachment by its ID.

        Parameters
        ----------
        attachment_id : str
            The ID of the attachment to delete.

        Raises
        ------
        GPPClientError
            If the deletion fails.
        """
        logger.debug("Deleting attachment %s", attachment_id)
        session = await self.rest_client._get_session()
        url = f"/attachment/{attachment_id}"

        try:
            async with session.delete(url) as response:
                text = await response.text()

                if response.status not in {200, 204}:
                    raise GPPClientError(
                        f"Failed to delete attachment {attachment_id} "
                        f"(status={response.status}): {text}"
                    )

                logger.debug(
                    "Deleted attachment %s",
                    attachment_id,
                )
        except Exception as exc:
            self.raise_error(GPPClientError, exc)

    async def update_by_id(
        self,
        attachment_id: str,
        *,
        file_name: str,
        description: str | None = None,
        file_path: str | Path | None = None,
        content: bytes | None = None,
    ) -> None:
        """
        Update an attachment by its ID.

        Parameters
        ----------
        attachment_id : str
            The ID of the attachment to update.
        file_name : str
            The new file name for the attachment. This is required.
        description : str | None, optional
            The new description for the attachment.
        file_path : str | Path | None, optional
            The path to the new file content for the attachment.
        content : bytes | None, optional
            The new file content as bytes.

        Raises
        ------
        GPPClientError
            If the update fails.
        GPPValidationError
            If a validation error occurs.
        """
        logger.debug("Updating attachment %s", attachment_id)
        body = self.resolve_content(file_path=file_path, content=content)
        # File name is required.
        params: dict[str, str] = {"fileName": file_name}

        if description is not None and description.strip() != "":
            params["description"] = description.strip()

        session = await self.rest_client._get_session()
        url = f"/attachment/{attachment_id}"

        try:
            async with session.put(url, params=params, data=body) as response:
                text = await response.text()

                if response.status not in {200, 201}:
                    raise GPPClientError(
                        f"Failed to update attachment {attachment_id} "
                        f"(status={response.status}): {text}"
                    )
                logger.debug(
                    "Updated attachment %s with status %s",
                    attachment_id,
                    response.status,
                )
        except Exception as exc:
            self.raise_error(GPPClientError, exc)

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
        url = f"/attachment/url/{attachment_id}"

        try:
            async with session.get(url, raise_for_status=True) as response:
                download_url = await response.text()
        except Exception as exc:
            self.raise_error(GPPClientError, exc)

        return download_url

    async def download_by_id(
        self,
        attachment_id: str,
        save_to: str | Path | None = None,
        overwrite: bool = False,
        chunk_size: int = 1024 * 1024,
    ) -> Path:
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

        Returns
        -------
        Path
            The path to the downloaded file.
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

            return path

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
