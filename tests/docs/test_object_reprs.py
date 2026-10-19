"""
Tests for the Sphinx extension that hides default object reprs as values.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(
    0, str(Path(__file__).resolve().parents[2] / "docs" / "source" / "_ext")
)

from object_reprs import is_object_repr_value  # noqa: E402


@pytest.mark.parametrize(
    "text",
    [
        " = <gpp_client.generated.custom_typing_fields.AddEventBatchResultGraphQLField object>",
        " = <gpp_client.Foo object at 0x10a2b3c40>",
        "= <Foo object>",
    ],
)
def test_default_object_repr_values_are_found(text):
    assert is_object_repr_value(text)


@pytest.mark.parametrize(
    "text",
    [
        " = 'production'",
        " = None",
        " = <GPPEnvironment.PRODUCTION: 'production'>",
        ": <Foo object>",
        "",
    ],
)
def test_meaningful_values_are_kept(text):
    assert not is_object_repr_value(text)
