from pathlib import Path

import pytest

from scripts.run_codegen import BuildPaths
from scripts.schema_merge import DEVELOPMENT, PRODUCTION, merge_schemas


def committed_schema(environment: str) -> str:
    """Return one environment's committed schema."""
    path = BuildPaths.for_repo(Path(__file__).parents[1]).schema_path(environment)
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def schema_str() -> str:
    """Merge the committed schemas, as the build does, and return the SDL."""
    return merge_schemas(
        development=committed_schema(DEVELOPMENT),
        production=committed_schema(PRODUCTION),
    ).sdl
