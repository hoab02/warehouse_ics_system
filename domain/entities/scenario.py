from datetime import datetime, timezone
from typing import Optional
from domain.fsm.scenario_fsm import ScenarioStatus


# class Scenario:
#     def __init__(self, scenario_id: str, scenario_type: str, stations: list, tasks: list, created_at: Optional[datetime] = None):
#         self.scenario_id = scenario_id
#         self.tasks = sorted(tasks, key=lambda t: t.sequence)
#         self.stations = stations
#         self.scenario_type = scenario_type
#         self.status = ScenarioStatus.CREATED
#         self.created_at = created_at or datetime.now(timezone.utc)

class Scenario:
    def __init__(self, scenario_id: str, scenario_type: str, tasks: list, created_at: Optional[datetime] = None):
        self.scenario_id = scenario_id
        self.tasks = sorted(tasks, key=lambda t: t.sequence)
        self.scenario_type = scenario_type
        self.status = ScenarioStatus.CREATED
        self.created_at = created_at or datetime.now(timezone.utc)