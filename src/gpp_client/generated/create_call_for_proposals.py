from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class CreateCallForProposals(BaseModel):
    create_call_for_proposals: "CreateCallForProposalsCreateCallForProposals" = Field(
        alias="createCallForProposals"
    )


class CreateCallForProposalsCreateCallForProposals(BaseModel):
    call_for_proposals: "CreateCallForProposalsCreateCallForProposalsCallForProposals" = Field(
        alias="callForProposals"
    )


class CreateCallForProposalsCreateCallForProposalsCallForProposals(
    CallForProposalsDetails
):
    pass


CreateCallForProposals.model_rebuild()
CreateCallForProposalsCreateCallForProposals.model_rebuild()
