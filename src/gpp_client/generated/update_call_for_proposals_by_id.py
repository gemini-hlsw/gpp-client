from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class UpdateCallForProposalsById(BaseModel):
    update_calls_for_proposals: "UpdateCallForProposalsByIdUpdateCallsForProposals" = (
        Field(alias="updateCallsForProposals")
    )


class UpdateCallForProposalsByIdUpdateCallsForProposals(BaseModel):
    has_more: bool = Field(alias="hasMore")
    calls_for_proposals: list[
        "UpdateCallForProposalsByIdUpdateCallsForProposalsCallsForProposals"
    ] = Field(alias="callsForProposals")


class UpdateCallForProposalsByIdUpdateCallsForProposalsCallsForProposals(
    CallForProposalsDetails
):
    pass


UpdateCallForProposalsById.model_rebuild()
UpdateCallForProposalsByIdUpdateCallsForProposals.model_rebuild()
