__all__ = ["AttachmentManager"]

from pathlib import Path


class AttachmentManager:
    _DEV_URL = "https://lucuma-postgres-odb-dev.herokuapp.com/attachment/url/"
    _STAGING_URL = "https://lucuma-postgres-odb-staging.herokuapp.com/attachment/url/"
    _PRODUCTION_URL = (
        "https://lucuma-postgres-odb-production.herokuapp.com/attachment/url/"
    )

    async def download(self, *, attachment_id: str, save_to: str | Path) -> None:
        pass

    async def get_url(self, *, attachment_id: str) -> str:
        return "Test"
