from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class UpdateCallsForProposals(BaseModel):
    update_calls_for_proposals: "UpdateCallsForProposalsUpdateCallsForProposals" = (
        Field(alias="updateCallsForProposals")
    )


class UpdateCallsForProposalsUpdateCallsForProposals(BaseModel):
    has_more: bool = Field(alias="hasMore")
    calls_for_proposals: list[
        "UpdateCallsForProposalsUpdateCallsForProposalsCallsForProposals"
    ] = Field(alias="callsForProposals")


class UpdateCallsForProposalsUpdateCallsForProposalsCallsForProposals(
    CallForProposalsDetails
):
    pass


UpdateCallsForProposals.model_rebuild()
UpdateCallsForProposalsUpdateCallsForProposals.model_rebuild()
