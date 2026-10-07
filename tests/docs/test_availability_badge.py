"""
Tests for the Sphinx extension that shows availability as a badge.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "docs" / "source" / "_ext")
)

from availability_badge import badge_lines, badge_parts, pills  # noqa: E402


def test_availability_line_becomes_a_badge_and_the_description_stays():
    lines = ["Available on: development.", "", "Which steps to copy."]

    badge_lines(lines)

    assert lines == [
        ":availability:`Available on: development`",
        "",
        "Which steps to copy.",
    ]


@pytest.mark.parametrize(
    "lines",
    [
        [],
        ["Return the program."],
        ["See Available on: development. in the notes."],
    ],
)
def test_docstrings_without_a_leading_availability_line_are_unchanged(lines):
    before = list(lines)

    badge_lines(lines)

    assert lines == before


def test_one_environment_shows_one_pill_with_its_own_class():
    assert pills("Available on: development") == [
        ("development", ["availability-pill", "availability-development"])
    ]


def test_two_environments_show_two_pills_each_with_its_own_class():
    assert pills("Available on: development, production") == [
        ("development", ["availability-pill", "availability-development"]),
        ("production", ["availability-pill", "availability-production"]),
    ]


def test_text_that_is_not_an_environment_name_shows_one_neutral_pill():
    assert pills("Available on: no environment (yet)") == [
        ("no environment (yet)", ["availability-pill"])
    ]


def test_two_pills_copy_as_a_comma_separated_list():
    parts = badge_parts("Available on: development, production")

    assert "".join(text for text, _ in parts) == "development, production"
    assert parts[1] == (", ", ["availability-separator"])


def test_one_pill_has_no_separator():
    assert badge_parts("Available on: development") == [
        ("development", ["availability-pill", "availability-development"])
    ]
