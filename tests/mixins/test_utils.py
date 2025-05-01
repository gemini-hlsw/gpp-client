import json
import pytest
from pathlib import Path
from typing import Any
from gpp_client.mixins.utils import (
    create_program_id_filter,
    merge_set_values,
    build_input_values,
    build_selector_values,
)


class TestCreateProgramIdFilter:
    """Tests for `create_program_id_filter`."""

    def test_returns_correct_filter(self):
        """Returns expected structure for a given program ID."""
        result = create_program_id_filter("p-2025A-001")
        assert result == {"program": {"id": {"EQ": "p-2025A-001"}}}


class TestMergeSetValues:
    """Tests for `merge_set_values`."""

    def test_no_file_returns_original(self):
        """Returns original values if no file is provided."""
        base = {"a": 1}
        result = merge_set_values(base.copy(), from_json_file=None)
        assert result == base

    def test_merges_file_values_on_top(self, tmp_path: Path):
        """Correctly merges file values into base."""
        json_path = tmp_path / "set.json"
        json_path.write_text(json.dumps({"b": 2, "c": 4}))

        base = {"a": 1, "c": 3}
        result = merge_set_values(base, from_json_file=json_path)
        assert result == {"a": 1, "b": 2, "c": 4}

    def test_raises_if_file_not_exists(self):
        """Raises ValueError if the file does not exist."""
        with pytest.raises(ValueError, match="JSON file does not exist"):
            merge_set_values({}, from_json_file="nonexistent.json")

    def test_raises_if_json_is_not_dict(self, tmp_path: Path):
        """Raises ValueError if JSON is not an object."""
        json_path = tmp_path / "bad.json"
        json_path.write_text(json.dumps(["not", "a", "dict"]))

        with pytest.raises(ValueError, match="JSON must be an object"):
            merge_set_values({}, from_json_file=json_path)

    def test_raises_if_json_invalid(self, tmp_path: Path):
        """Raises ValueError on malformed JSON."""
        bad_path = tmp_path / "bad.json"
        bad_path.write_text("{invalid json}")

        with pytest.raises(ValueError, match="Invalid JSON"):
            merge_set_values({}, from_json_file=bad_path)


class TestBuildInputValues:
    """Tests for `build_input_values`."""

    @pytest.mark.parametrize(
        "kwargs,expected",
        [
            (
                {},
                {},
            ),
            (
                {"set_values": {"a": 1}},
                {
                    "SET": {"a": 1},
                },
            ),
            (
                {
                    "set_values": {"a": 1},
                    "identifier": {"programId": "p-1"},
                    "where": {"id": {"EQ": "x"}},
                    "limit": 10,
                    "include_deleted": True,
                },
                {
                    "SET": {"a": 1},
                    "programId": "p-1",
                    "WHERE": {"id": {"EQ": "x"}},
                    "LIMIT": 10,
                    "includeDeleted": True,
                },
            ),
        ],
    )
    def test_builds_expected_input_dict(
        self, kwargs: dict[str, Any], expected: dict[str, Any]
    ):
        """Correctly builds input dictionary from keyword args."""
        result = build_input_values(**kwargs)
        assert result == expected


class TestBuildSelectorValues:
    """Tests for `build_selector_values`."""

    @pytest.mark.parametrize(
        "kwargs,expected",
        [
            (
                {},
                {
                    "where": None,
                    "limit": None,
                    "offset": None,
                },
            ),
            (
                {
                    "identifier": {"targetId": "t-123"},
                    "where": {"name": {"LIKE": "abc"}},
                    "limit": 100,
                    "offset": "t-100",
                    "include_deleted": True,
                },
                {
                    "targetId": "t-123",
                    "where": {"name": {"LIKE": "abc"}},
                    "limit": 100,
                    "offset": "t-100",
                    "includeDeleted": True,
                },
            ),
        ],
    )
    def test_builds_expected_selector_dict(
        self, kwargs: dict[str, Any], expected: dict[str, Any]
    ):
        """Correctly builds selector dictionary from keyword args."""
        result = build_selector_values(**kwargs)
        assert result == expected
