from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .fragments import ProgramDetail


class RestoreProgramById(BaseModel):
    update_programs: "RestoreProgramByIdUpdatePrograms" = Field(alias="updatePrograms")


class RestoreProgramByIdUpdatePrograms(BaseModel):
    has_more: bool = Field(alias="hasMore")
    programs: list["RestoreProgramByIdUpdateProgramsPrograms"]


class RestoreProgramByIdUpdateProgramsPrograms(ProgramDetail):
    all_group_elements: list[
        "RestoreProgramByIdUpdateProgramsProgramsAllGroupElements"
    ] = Field(alias="allGroupElements")


class RestoreProgramByIdUpdateProgramsProgramsAllGroupElements(BaseModel):
    parent_group_id: Optional[Any] = Field(alias="parentGroupId")
    observation: Optional[
        "RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsObservation"
    ]
    group: Optional["RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroup"]


class RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsObservation(BaseModel):
    id: Any
    group_id: Optional[Any] = Field(alias="groupId")


class RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroup(BaseModel):
    id: Any
    name: Optional[Any]
    minimum_required: Optional[Any] = Field(alias="minimumRequired")
    ordered: bool
    parent_id: Optional[Any] = Field(alias="parentId")
    parent_index: Any = Field(alias="parentIndex")
    minimum_interval: Optional[
        "RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMinimumInterval"
    ] = Field(alias="minimumInterval")
    maximum_interval: Optional[
        "RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMaximumInterval"
    ] = Field(alias="maximumInterval")
    system: bool


class RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMinimumInterval(
    BaseModel
):
    seconds: Any


class RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroupMaximumInterval(
    BaseModel
):
    seconds: Any


RestoreProgramById.model_rebuild()
RestoreProgramByIdUpdatePrograms.model_rebuild()
RestoreProgramByIdUpdateProgramsPrograms.model_rebuild()
RestoreProgramByIdUpdateProgramsProgramsAllGroupElements.model_rebuild()
RestoreProgramByIdUpdateProgramsProgramsAllGroupElementsGroup.model_rebuild()
