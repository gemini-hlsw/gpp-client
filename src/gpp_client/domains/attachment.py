__all__ = ["AttachmentDomain"]

import logging
from pathlib import Path
from urllib.parse import urlparse

from aiohttp import ClientHandlerType, ClientRequest, ClientResponse

from gpp_client.domains.base import BaseDomain
from gpp_client.exceptions import GPPClientError, GPPResponseError
from gpp_client.generated.enums import AttachmentType
from gpp_client.generated.get_observation_attachments_by_id import (
    GetObservationAttachmentsById,
)
from gpp_client.generated.get_observation_attachments_by_reference import (
    GetObservationAttachmentsByReference,
)
from gpp_client.generated.get_program_attachments_by_id import (
    GetProgramAttachmentsById,
)
from gpp_client.generated.get_program_attachments_by_proposal_reference import (
    GetProgramAttachmentsByProposalReference,
)
from gpp_client.generated.get_program_attachments_by_reference import (
    GetProgramAttachmentsByReference,
)

logger = logging.getLogger(__name__)

DEFAULT_OK: set[int] = {200}
UPLOAD_OK: set[int] = {200, 201}
UPDATE_OK: set[int] = {200, 201}
DELETE_OK: set[int] = {200, 204}


class AttachmentDomain(BaseDomain):
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

        params = _build_upload_params(
            program_id=program_id,
            attachment_type=attachment_type,
            file_name=file_name,
            description=description,
        )

        session = await self._rest.get_session()
        url = "/attachment"

        try:
            async with session.post(url, params=params, data=body) as response:
                await self.raise_for_status(response, ok_statuses=UPLOAD_OK)
                text = await response.text()

                attachment_id = text.strip()
                if not attachment_id:
                    raise GPPClientError(
                        "Upload attachment returned an empty attachment id."
                    )

                logger.debug("Uploaded attachment id=%s", attachment_id)
                return attachment_id

        except GPPResponseError:
            raise
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
        session = await self._rest.get_session()
        url = f"/attachment/{attachment_id}"

        try:
            async with session.delete(url) as response:
                await self.raise_for_status(response, ok_statuses=DELETE_OK)

                logger.debug(
                    "Deleted attachment %s",
                    attachment_id,
                )
        except GPPResponseError:
            raise
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
        params = _build_update_params(file_name=file_name, description=description)

        session = await self._rest.get_session()
        url = f"/attachment/{attachment_id}"

        try:
            async with session.put(url, params=params, data=body) as response:
                await self.raise_for_status(response, ok_statuses=UPDATE_OK)

                logger.debug(
                    "Updated attachment %s",
                    attachment_id,
                )
        except GPPResponseError:
            raise
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
        session = await self._rest.get_session()
        url = f"/attachment/url/{attachment_id}"

        try:
            async with session.get(url) as response:
                await self.raise_for_status(response, ok_statuses=DEFAULT_OK)
                download_url = await response.text()
        except GPPResponseError:
            raise
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
        session = await self._rest.get_session()
        download_url = await self.get_download_url_by_id(attachment_id)

        # Get the filename and resolve the destination directory.
        filename = _filename_from_presigned_url(download_url)
        dest_dir = _resolve_download_dir(save_to)
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
                middlewares=(_remove_headers_middleware,),
            ) as response:
                await self.raise_for_status(response, ok_statuses=DEFAULT_OK)

                # Download the file in chunks to avoid loading it all into memory.
                with path.open("wb") as fh:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        fh.write(chunk)

                logger.info("Downloaded %s", path)

            return path

        except GPPResponseError:
            raise
        except Exception as exc:
            self.raise_error(GPPClientError, exc, include_traceback=True)

    async def get_all_by_observation_id(
        self,
        observation_id: str,
    ) -> GetObservationAttachmentsById:
        """
        Get all attachments for an observation by observation ID.

        Parameters
        ----------
        observation_id : str
            The observation ID.

        Returns
        -------
        GetObservationAttachmentsById
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation_attachments_by_id(
            observation_id=observation_id
        )

    async def get_all_by_observation_reference(
        self,
        observation_reference: str,
    ) -> GetObservationAttachmentsByReference:
        """
        Get all attachments for an observation by observation reference.

        Parameters
        ----------
        observation_reference : str
            The observation reference label.

        Returns
        -------
        GetObservationAttachmentsByReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_observation_attachments_by_reference(
            observation_reference=observation_reference
        )

    async def get_all_by_program_id(
        self,
        program_id: str,
    ) -> GetProgramAttachmentsById:
        """
        Get all attachments for a program by program ID.

        Parameters
        ----------
        program_id : str
            The program ID.

        Returns
        -------
        GetProgramAttachmentsById
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_attachments_by_id(program_id=program_id)

    async def get_all_by_program_reference(
        self,
        program_reference: str,
    ) -> GetProgramAttachmentsByReference:
        """
        Get all attachments for a program by program reference.

        Parameters
        ----------
        program_reference : str
            The program reference label.

        Returns
        -------
        GetProgramAttachmentsByReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_attachments_by_program_reference(
            program_reference=program_reference
        )

    async def get_all_by_proposal_reference(
        self,
        proposal_reference: str,
    ) -> GetProgramAttachmentsByProposalReference:
        """
        Get all attachments for a program by proposal reference.

        Parameters
        ----------
        proposal_reference : str
            The proposal reference label.

        Returns
        -------
        GetProgramAttachmentsByProposalReference
            The generated GraphQL response model.
        """
        return await self._graphql.get_program_attachments_by_proposal_reference(
            proposal_reference=proposal_reference
        )


async def _remove_headers_middleware(
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


def _filename_from_presigned_url(download_url: str) -> str:
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


def _resolve_download_dir(save_to: str | Path | None) -> Path:
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


def _build_upload_params(
    *,
    program_id: str,
    attachment_type: AttachmentType,
    file_name: str,
    description: str | None,
) -> dict[str, str]:
    """
    Build upload parameters for attachment upload.

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

    Returns
    -------
    dict[str, str]
        The parameters for the upload request.
    """
    params: dict[str, str] = {
        "programId": program_id,
        "fileName": file_name,
        "attachmentType": attachment_type.value,
    }
    if description and description.strip():
        params["description"] = description.strip()
    return params


def _build_update_params(*, file_name: str, description: str | None) -> dict[str, str]:
    """
    Build update parameters for attachment update.

    Parameters
    ----------
    file_name : str
        The new file name for the attachment.
    description : str | None
        The new description for the attachment.

    Returns
    -------
    dict[str, str]
        The parameters for the update request.
    """
    params: dict[str, str] = {"fileName": file_name}
    if description is not None and description.strip() != "":
        params["description"] = description.strip()
    return params
