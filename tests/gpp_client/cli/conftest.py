import re
from typing import Optional

import pytest
from typer.testing import CliRunner

runner = CliRunner()


@pytest.fixture(scope="module")
def cli_runner():
    return runner


class Helpers:
    @staticmethod
    def extract_first_resource_id(output: str, prefix: str) -> Optional[str]:
        """Extract the first resource ID with the given prefix from a rich table output.

        Parameters
        ----------
        output : str
            The table text.
        prefix : str
            The ID prefix to match (e.g., "p", "u", etc.).

        Returns
        -------
        str, optional
            The first matched ID, or None if not found.
        """
        pattern = re.compile(rf"│\s+({re.escape(prefix)}-[a-z0-9]+)\s+│")

        for line in output.splitlines():
            match = pattern.match(line)
            if match:
                return match.group(1)
        return None


@pytest.fixture
def helpers():
    return Helpers
