from importlib.resources import files

import pytest

from scripts.schema_merge import DEVELOPMENT, PRODUCTION, merge_schemas


def _committed_schema(environment: str) -> str:
    return files("gpp_client.schemas").joinpath(f"{environment}.graphql").read_text()


@pytest.fixture(scope="session")
def schema_str() -> str:
    """Merge the committed schemas, as the build does, and return the SDL."""
    return merge_schemas(
        development=_committed_schema(DEVELOPMENT),
        production=_committed_schema(PRODUCTION),
    ).sdl
