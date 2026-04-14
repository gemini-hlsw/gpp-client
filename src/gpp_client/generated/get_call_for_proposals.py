from typing import Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import CallForProposalsDetails


class GetCallForProposals(BaseModel):
    call_for_proposals: Optional["GetCallForProposalsCallForProposals"] = Field(
        alias="callForProposals"
    )


class GetCallForProposalsCallForProposals(CallForProposalsDetails):
    pass


GetCallForProposals.model_rebuild()
