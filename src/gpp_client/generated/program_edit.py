from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EditType, Existence


class ProgramEdit(BaseModel):
    program_edit: "ProgramEditProgramEdit" = Field(alias="programEdit")


class ProgramEditProgramEdit(BaseModel):
    edit_type: EditType = Field(alias="editType")
    value: "ProgramEditProgramEditValue"


class ProgramEditProgramEditValue(BaseModel):
    description: Optional[Any]
    existence: Existence
    name: Optional[Any]
    id: Any
    all_group_elements: list["ProgramEditProgramEditValueAllGroupElements"] = Field(
        alias="allGroupElements"
    )


class ProgramEditProgramEditValueAllGroupElements(BaseModel):
    observation: Optional["ProgramEditProgramEditValueAllGroupElementsObservation"]
    group: Optional["ProgramEditProgramEditValueAllGroupElementsGroup"]


class ProgramEditProgramEditValueAllGroupElementsObservation(BaseModel):
    id: Any


class ProgramEditProgramEditValueAllGroupElementsGroup(BaseModel):
    id: Any


ProgramEdit.model_rebuild()
ProgramEditProgramEdit.model_rebuild()
ProgramEditProgramEditValue.model_rebuild()
ProgramEditProgramEditValueAllGroupElements.model_rebuild()
