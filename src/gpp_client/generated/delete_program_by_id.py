from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ProgramDetail


class DeleteProgramById(BaseModel):
    update_programs: "DeleteProgramByIdUpdatePrograms" = Field(alias="updatePrograms")


class DeleteProgramByIdUpdatePrograms(BaseModel):
    has_more: bool = Field(alias="hasMore")
    programs: list["DeleteProgramByIdUpdateProgramsPrograms"]


class DeleteProgramByIdUpdateProgramsPrograms(ProgramDetail):
    all_group_elements: list[
        "DeleteProgramByIdUpdateProgramsProgramsAllGroupElements"
    ] = Field(alias="allGroupElements")


class DeleteProgramByIdUpdateProgramsProgramsAllGroupElements(BaseModel):
    parent_group_id: Optional[Any] = Field(alias="parentGroupId")
    observation: Optional[
        "DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsObservation"
    ]
    group: Optional["DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroup"]


class DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsObservation(BaseModel):
    id: Any
    group_id: Optional[Any] = Field(alias="groupId")


class DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroup(BaseModel):
    id: Any
    name: Optional[Any]
    minimum_required: Optional[Any] = Field(alias="minimumRequired")
    ordered: bool
    parent_id: Optional[Any] = Field(alias="parentId")
    parent_index: Any = Field(alias="parentIndex")
    minimum_interval: Optional[
        "DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMinimumInterval"
    ] = Field(alias="minimumInterval")
    maximum_interval: Optional[
        "DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMaximumInterval"
    ] = Field(alias="maximumInterval")
    system: bool


class DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMinimumInterval(
    BaseModel
):
    seconds: Any


class DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMaximumInterval(
    BaseModel
):
    seconds: Any


DeleteProgramById.model_rebuild()
DeleteProgramByIdUpdatePrograms.model_rebuild()
DeleteProgramByIdUpdateProgramsPrograms.model_rebuild()
DeleteProgramByIdUpdateProgramsProgramsAllGroupElements.model_rebuild()
DeleteProgramByIdUpdateProgramsProgramsAllGroupElementsGroup.model_rebuild()
