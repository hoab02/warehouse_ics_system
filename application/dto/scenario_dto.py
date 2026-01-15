from application.dto.task_dto import TaskDTO
from domain.entities.scenario import Scenario

# class ScenarioDTO:
#     def __init__(self, scenario_id, scenario_type, tasks: list):
#         self.id = scenario_id
#         self.type = scenario_type
#         self.tasks = tasks  # list[TaskDTO]
#
#     def to_domain(self):
#         return Scenario(
#             scenario_id=self.id,
#             scenario_type=self.type,
#             tasks=self.tasks
#         )

from pydantic import BaseModel
from typing import List

class ScenarioDTO(BaseModel):
    scenario_id: str
    type: str
    stations: List[str]
    tasks: List[TaskDTO]

    def to_domain(self):
        return Scenario(
            scenario_id=self.scenario_id,
            scenario_type=self.type,
            stations=self.stations,
            tasks=self.tasks
        )
