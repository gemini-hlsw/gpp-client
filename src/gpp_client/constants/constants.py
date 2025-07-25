__all__ = ["GPPConstants", "GPPEnvironment"]

from enum import Enum


class GPPEnvironment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"


class GPPConstants:
    GRAPHQL_ENDPOINT = "/odb"
    ATTACHMENT_ENDPOINT = "/attachment/url/"

    BASE_URLS = {
        GPPEnvironment.PRODUCTION: "https://lucuma-postgres-odb-production.herokuapp.com",
        GPPEnvironment.STAGING: "https://lucuma-postgres-odb-staging.herokuapp.com",
        GPPEnvironment.DEVELOPMENT: "https://lucuma-postgres-odb-dev.herokuapp.com",
    }

    @classmethod
    def graphql_url(cls, env: GPPEnvironment) -> str:
        return f"{cls.BASE_URLS[env]}{cls.GRAPHQL_ENDPOINT}"

    @classmethod
    def attachment_url(cls, env: GPPEnvironment, attachment_id: str) -> str:
        return f"{cls.BASE_URLS[env]}{cls.ATTACHMENT_ENDPOINT}{attachment_id}"
