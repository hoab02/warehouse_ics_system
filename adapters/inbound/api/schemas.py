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

class ReturnShelfPayload(BaseModel):
    scenario_id: str
    shelf_id: str
    logical_task_ids: str
    station_id: str
    side: str