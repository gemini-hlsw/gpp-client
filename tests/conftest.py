from importlib.resources import files

import pytest

from custom_plugins.environments import USER_ENVIRONMENTS
from scripts.schema_merge import merge_schemas


@pytest.fixture(scope="session")
def schema_str() -> str:
    """Merge the committed schemas, as the build does, and return the SDL."""
    return merge_schemas(
        {
            environment: files("gpp_client.schemas")
            .joinpath(f"{environment}.graphql")
            .read_text()
            for environment in USER_ENVIRONMENTS
        }
    ).sdl
