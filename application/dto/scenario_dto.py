from application.dto.task_dto import TaskDTO
from domain.entities.scenario import Scenario

from pydantic import BaseModel
from typing import List

class ScenarioDTO(BaseModel):
    scenario_id: str
    type: str
    # stations: List[str]
    tasks: List[TaskDTO]

    def to_domain(self):
        return Scenario(
            scenario_id=self.scenario_id,
            scenario_type=self.type,
            tasks=self.tasks,
        )
