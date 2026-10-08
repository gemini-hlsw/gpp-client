"""
Tests that the hand-written string enums behave as their values.
"""

import json
from enum import Enum

import pytest
from pydantic import TypeAdapter

from gpp_client.domains.site_status import Site
from gpp_client.environment import GPPEnvironment
from gpp_client.urls import Endpoint

_MEMBERS = [*GPPEnvironment, *Endpoint, *Site]


@pytest.mark.parametrize("member", _MEMBERS, ids=repr)
def test_member_equals_and_hashes_as_its_value(member: Enum) -> None:
    """
    Ensure a member compares and looks up as its plain string value.
    """
    assert member == member.value
    assert {member: "found"}[member.value] == "found"
    assert type(member)(member.value) is member


@pytest.mark.parametrize("member", _MEMBERS, ids=repr)
def test_member_serializes_as_its_value(member: Enum) -> None:
    """
    Ensure JSON and pydantic write a member as its value and read it back.
    """
    adapter = TypeAdapter(type(member))

    assert json.dumps(member) == json.dumps(member.value)
    assert adapter.dump_python(member, mode="json") == member.value
    assert adapter.validate_python(member.value) is member


@pytest.mark.parametrize("member", _MEMBERS, ids=repr)
def test_member_prints_as_its_value(member: Enum) -> None:
    """
    Ensure ``str`` and f-strings give the value, not the class-qualified name.
    """
    assert str(member) == member.value
    assert f"{member}" == member.value
