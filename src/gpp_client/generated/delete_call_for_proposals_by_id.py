from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class DeleteCallForProposalsById(BaseModel):
    update_calls_for_proposals: "DeleteCallForProposalsByIdUpdateCallsForProposals" = (
        Field(alias="updateCallsForProposals")
    )


class DeleteCallForProposalsByIdUpdateCallsForProposals(BaseModel):
    has_more: bool = Field(alias="hasMore")
    calls_for_proposals: list[
        "DeleteCallForProposalsByIdUpdateCallsForProposalsCallsForProposals"
    ] = Field(alias="callsForProposals")


class DeleteCallForProposalsByIdUpdateCallsForProposalsCallsForProposals(
    CallForProposalsDetails
):
    pass


DeleteCallForProposalsById.model_rebuild()
DeleteCallForProposalsByIdUpdateCallsForProposals.model_rebuild()
