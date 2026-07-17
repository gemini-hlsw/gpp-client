"""
Tests for REST response models and parsers.
"""

from datetime import datetime, timezone

from gpp_client.rest.models import VisibilityChanges, parse_visibility_changes


def test_parse_mixed_observations_and_targets() -> None:
    """
    Ensure o- and t- GIDs are routed to the right sets.
    """
    body = (
        "o-123\t2026-07-15T10:00:00Z\n"
        "t-456\t2026-07-15T11:30:00Z\n"
        "o-789\t2026-07-15T09:15:00Z\n"
    )

    result = parse_visibility_changes(body)

    assert result.observation_ids == frozenset({"o-123", "o-789"})
    assert result.target_ids == frozenset({"t-456"})
    assert result.max_timestamp == datetime(2026, 7, 15, 11, 30, tzinfo=timezone.utc)


def test_parse_empty_body() -> None:
    """
    Ensure an empty body yields an empty result.
    """
    result = parse_visibility_changes("")

    assert result == VisibilityChanges()
    assert result.max_timestamp is None


def test_parse_skips_blank_lines_and_unknown_prefixes() -> None:
    """
    Ensure blank lines and unknown GID prefixes are skipped.
    """
    body = "\nx-999\t2026-07-15T10:00:00Z\no-123\t2026-07-15T10:00:00Z\n   \n"

    result = parse_visibility_changes(body)

    assert result.observation_ids == frozenset({"o-123"})
    assert result.target_ids == frozenset()


def test_parse_keeps_gid_when_timestamp_is_bad() -> None:
    """
    Ensure a bad timestamp keeps the GID but not the timestamp.
    """
    body = "t-456\tnot-a-timestamp\n"

    result = parse_visibility_changes(body)

    assert result.target_ids == frozenset({"t-456"})
    assert result.max_timestamp is None


def test_parse_keeps_gid_when_timestamp_is_missing() -> None:
    """
    Ensure a line without a tab separator keeps the GID.
    """
    body = "o-123\n"

    result = parse_visibility_changes(body)

    assert result.observation_ids == frozenset({"o-123"})
    assert result.max_timestamp is None


def test_parse_handles_offset_timestamps() -> None:
    """
    Ensure explicit-offset ISO8601 timestamps parse.
    """
    body = "o-123\t2026-07-15T10:00:00+00:00\n"

    result = parse_visibility_changes(body)

    assert result.max_timestamp == datetime(2026, 7, 15, 10, 0, tzinfo=timezone.utc)
