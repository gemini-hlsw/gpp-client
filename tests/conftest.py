from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def schema_str() -> str:
    """Load the full schema.graphql content as a string."""
    schema_path = Path(__file__).parent.parent / "schema.graphql"
    return schema_path.read_text()
