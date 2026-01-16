from pydantic import BaseModel
from typing import List

class TaskPayload(BaseModel):
    sequence: int
    shelf_id: str
    station_id: str
    side: str


class ScenarioPayload(BaseModel):
    scenario_id: str
    type: str
    stations: List[str]
    tasks: List[TaskPayload]

class RcsCallbackPayload(BaseModel):
    mission_id: str
    status: str