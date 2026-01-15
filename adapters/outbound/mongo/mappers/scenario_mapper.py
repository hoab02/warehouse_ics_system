from adapters.outbound.mongo.mappers.task_mapper import TaskMapper
from domain.entities.scenario import Scenario


class ScenarioMapper:

    @staticmethod
    def to_document(s: Scenario) -> dict:
        return {
            "scenario_id": s.scenario_id,
            "type": s.scenario_type,
            "status": s.status,
            "tasks":[
                TaskMapper.to_document(t) for t in s.tasks
            ]
        }

    @staticmethod
    def from_document(doc: dict) -> Scenario:
        scenario = Scenario(doc["scenario_id"], doc["type"], doc["station"], doc["tasks"])
        scenario.status = doc["status"]
        return scenario