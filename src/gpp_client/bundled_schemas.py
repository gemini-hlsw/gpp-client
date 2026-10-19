"""
The schema each environment's copy of the client was built from.

The build records the date and digest of every committed environment schema
in ``gpp_client.generated.bundled_schemas``. Error messages name the date so
a user can tell an install that is behind the server from a wrong environment
or wrong data.
"""

__all__ = ["BundledSchema", "bundled_schema"]

from dataclasses import dataclass

from gpp_client.environment import GPPEnvironment
from gpp_client.generated_tables import load_generated


@dataclass(frozen=True)
class BundledSchema:
    """
    One environment's schema as the client was built from it.

    Attributes
    ----------
    environment : GPPEnvironment
        The environment the schema belongs to.
    date : str | None
        The day the schema was introspected, as ``YYYY-MM-DD``, or ``None``
        when the committed schema carries no date.
    sha256 : str
        The hex SHA-256 digest of the committed schema file.
    """

    environment: GPPEnvironment
    date: str | None
    sha256: str

    def __str__(self) -> str:
        """
        Return the schema as an error message names it.

        Returns
        -------
        str
            ``"the development schema of <date>"``, or the digest's first
            twelve characters when the schema has no date.
        """
        label = self.environment.label
        if self.date is None:
            return f"the {label} schema {self.sha256[:12]}"
        return f"the {label} schema of {self.date}"


def bundled_schema(environment: GPPEnvironment) -> BundledSchema:
    """
    Return the schema the client was built from for one environment.

    Parameters
    ----------
    environment : GPPEnvironment
        The environment.

    Returns
    -------
    BundledSchema
        Its date and digest, as the build recorded them.
    """
    entry = load_generated("bundled_schemas").SCHEMAS[environment.label]
    return BundledSchema(environment, entry["date"], entry["sha256"])
