from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class RestoreCallForProposalsById(BaseModel):
    update_calls_for_proposals: "RestoreCallForProposalsByIdUpdateCallsForProposals" = (
        Field(alias="updateCallsForProposals")
    )


class RestoreCallForProposalsByIdUpdateCallsForProposals(BaseModel):
    has_more: bool = Field(alias="hasMore")
    calls_for_proposals: list[
        "RestoreCallForProposalsByIdUpdateCallsForProposalsCallsForProposals"
    ] = Field(alias="callsForProposals")


RestoreCallForProposalsByIdUpdateCallsForProposalsCallsForProposals = (
    CallForProposalsDetails
)
RestoreCallForProposalsById.model_rebuild()
RestoreCallForProposalsByIdUpdateCallsForProposals.model_rebuild()
