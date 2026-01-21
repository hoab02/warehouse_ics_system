from pydantic import BaseModel
from typing import List

# class TaskPayload(BaseModel):
#     sequence: int
#     shelf_id: str
#     station_id: str
#     side: str

class TaskPayload(BaseModel):
    sequence: int
    picking_session_code: str
    picking_task_code: str
    or_code: str
    shelf_code: str
    station_code: str
    side_code: str


class ScenarioPayload(BaseModel):
    scenario_id: str
    type: str
    # stations: List[str]
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