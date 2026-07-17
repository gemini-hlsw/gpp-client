"""
Models and parsers for REST API responses.
"""

__all__ = ["VisibilityChanges", "parse_visibility_changes"]

import logging
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class VisibilityChanges:
    """
    Observations and targets whose visibility-relevant inputs changed.

    Attributes
    ----------
    observation_ids : frozenset[str]
        Observation GIDs (``o-`` prefix) with visibility changes.
    target_ids : frozenset[str]
        Target GIDs (``t-`` prefix) with visibility changes.
    max_timestamp : datetime | None
        Latest change timestamp reported by the endpoint, or None when no
        parseable timestamps were returned.
    """

    observation_ids: frozenset[str] = field(default_factory=frozenset)
    target_ids: frozenset[str] = field(default_factory=frozenset)
    max_timestamp: datetime | None = None


def parse_visibility_changes(body: str) -> VisibilityChanges:
    """
    Parse the TSV body of ``/scheduler/visibility-changes``.

    Each line is ``<gid>\\t<iso8601-timestamp>`` where the GID prefix
    disambiguate the entity: ``o-`` for observations, ``t-`` for targets.
    Malformed lines and unknown prefixes are skipped with a warning; a bad
    timestamp keeps the GID but does not contribute to ``max_timestamp``.

    Parameters
    ----------
    body : str
        Raw TSV response body.

    Returns
    -------
    VisibilityChanges
        Parsed observation/target GIDs and the latest change timestamp.
    """
    observation_ids: set[str] = set()
    target_ids: set[str] = set()
    max_timestamp: datetime | None = None

    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        gid, _, raw_timestamp = line.partition("\t")
        gid = gid.strip()

        if gid.startswith("o-"):
            observation_ids.add(gid)
        elif gid.startswith("t-"):
            target_ids.add(gid)
        else:
            logger.warning(
                "Skipping visibility-changes line with unknown GID: %r", line
            )
            continue

        try:
            timestamp = datetime.fromisoformat(
                raw_timestamp.strip().replace("Z", "+00:00")
            )
        except ValueError:
            logger.warning("Unparseable timestamp in visibility-changes line: %r", line)
            continue
        if max_timestamp is None or timestamp > max_timestamp:
            max_timestamp = timestamp

    return VisibilityChanges(
        observation_ids=frozenset(observation_ids),
        target_ids=frozenset(target_ids),
        max_timestamp=max_timestamp,
    )
