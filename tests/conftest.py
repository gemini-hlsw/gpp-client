from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def schema_str() -> str:
    """Load the committed merged schema as a string."""
    schema_path = Path(__file__).parents[1] / "graphql" / "schemas" / "merged.graphql"
    return schema_path.read_text()
