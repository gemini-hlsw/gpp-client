from typing import Any

from .base_model import BaseModel


class Ping(BaseModel):
    programs: "PingPrograms"


class PingPrograms(BaseModel):
    matches: list["PingProgramsMatches"]


class PingProgramsMatches(BaseModel):
    id: Any


Ping.model_rebuild()
PingPrograms.model_rebuild()
