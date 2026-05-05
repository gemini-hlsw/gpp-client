from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import EditType


class TargetEdit(BaseModel):
    target_edit: "TargetEditTargetEdit" = Field(alias="targetEdit")


class TargetEditTargetEdit(BaseModel):
    edit_type: EditType = Field(alias="editType")
    target_id: Any = Field(alias="targetId")
    value: Optional["TargetEditTargetEditValue"]


class TargetEditTargetEditValue(BaseModel):
    id: Any
    name: Any
    nonsidereal: Optional["TargetEditTargetEditValueNonsidereal"]
    sidereal: Optional["TargetEditTargetEditValueSidereal"]


class TargetEditTargetEditValueNonsidereal(BaseModel):
    des: str
    key: str


class TargetEditTargetEditValueSidereal(BaseModel):
    ra: "TargetEditTargetEditValueSiderealRa"
    dec: "TargetEditTargetEditValueSiderealDec"


class TargetEditTargetEditValueSiderealRa(BaseModel):
    degrees: Any


class TargetEditTargetEditValueSiderealDec(BaseModel):
    degrees: Any


TargetEdit.model_rebuild()
TargetEditTargetEdit.model_rebuild()
TargetEditTargetEditValue.model_rebuild()
TargetEditTargetEditValueSidereal.model_rebuild()
