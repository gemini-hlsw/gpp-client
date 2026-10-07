"""
Tests that responses carrying enum values the client has never seen still parse.
"""

import pytest

from gpp_client.generated.enums import ProgramType, ProposalStatus


def _programs_response(proposal_status: str, program_type: str = "SCIENCE") -> dict:
    return {
        "programs": {
            "matches": [
                {
                    "id": "p-1",
                    "name": None,
                    "description": None,
                    "reference": None,
                    "proposalStatus": proposal_status,
                    "type": program_type,
                }
            ],
            "hasMore": False,
        }
    }


@pytest.mark.asyncio
async def test_unknown_enum_value_parses_as_member_with_raw_value(
    gpp_client,
    gpp_transport,
) -> None:
    """
    Ensure an enum value GPP added after this build parses as a member.
    """
    gpp_transport.respond(_programs_response("NEWLY_PROMOTED"))

    result = await gpp_client.goats.get_programs()

    [program] = result.programs.matches
    assert isinstance(program.proposal_status, ProposalStatus)
    assert program.proposal_status.value == "NEWLY_PROMOTED"
    assert program.proposal_status == "NEWLY_PROMOTED"


@pytest.mark.asyncio
async def test_repeated_unknown_value_returns_same_member(
    gpp_client,
    gpp_transport,
) -> None:
    """
    Ensure two responses with the same unknown value share one member.
    """
    gpp_transport.respond(_programs_response("SUBMITTED", "BRAND_NEW_TYPE"))
    gpp_transport.respond(_programs_response("SUBMITTED", "BRAND_NEW_TYPE"))

    first = await gpp_client.goats.get_programs()
    second = await gpp_client.goats.get_programs()

    assert first.programs.matches[0].type_ is second.programs.matches[0].type_
    assert first.programs.matches[0].type_ is ProgramType("BRAND_NEW_TYPE")


@pytest.mark.asyncio
async def test_known_values_parse_unchanged(gpp_client, gpp_transport) -> None:
    """
    Ensure known values still parse to their declared members.
    """
    gpp_transport.respond(_programs_response("ACCEPTED", "SCIENCE"))

    result = await gpp_client.goats.get_programs()

    [program] = result.programs.matches
    assert program.proposal_status is ProposalStatus.ACCEPTED
    assert program.type_ is ProgramType.SCIENCE


@pytest.mark.asyncio
async def test_unknown_member_keeps_raw_value_when_dumped(
    gpp_client,
    gpp_transport,
) -> None:
    """
    Ensure an unknown member serializes back to the raw value GPP sent.
    """
    gpp_transport.respond(_programs_response("UNDER_REVIEW"))

    result = await gpp_client.goats.get_programs()

    dumped = result.model_dump(mode="json", by_alias=True)
    assert dumped["programs"]["matches"][0]["proposalStatus"] == "UNDER_REVIEW"
    assert "UNDER_REVIEW" not in [member.value for member in ProposalStatus]


def test_non_string_values_are_still_rejected() -> None:
    """
    Ensure only string values become members, as GPP enums are strings.
    """
    with pytest.raises(ValueError):
        ProposalStatus(3)
