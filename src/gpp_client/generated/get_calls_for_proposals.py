from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class GetCallsForProposals(BaseModel):
    calls_for_proposals: "GetCallsForProposalsCallsForProposals" = Field(
        alias="callsForProposals"
    )


class GetCallsForProposalsCallsForProposals(BaseModel):
    has_more: bool = Field(alias="hasMore")
    matches: list["GetCallsForProposalsCallsForProposalsMatches"]


class GetCallsForProposalsCallsForProposalsMatches(CallForProposalsDetails):
    pass


GetCallsForProposals.model_rebuild()
GetCallsForProposalsCallsForProposals.model_rebuild()
