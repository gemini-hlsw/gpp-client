"""
Tests for the Sphinx extension that lists a page's classes in a table.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "docs" / "source" / "_ext")
)

from class_index import first_sentence  # noqa: E402


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Return the program. Then more.", "Return the program."),
        ("Return the program.", "Return the program."),
        ("No full stop", "No full stop"),
        ("Line one\ncontinues here. Next.", "Line one continues here."),
        ("Use e.g. this. Next.", "Use e.g. this."),
        ("The ID, such as p-10a.", "The ID, such as p-10a."),
        ("", ""),
    ],
)
def test_first_sentence_keeps_only_the_first_sentence(text, expected):
    assert first_sentence(text) == expected
