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
            ],
            "created_at": s.created_at
        }

    @staticmethod
    def from_document(doc: dict) -> Scenario:
        tasks = [
            TaskMapper.from_document(t)
            for t in doc.get("tasks", [])
        ]

        # station_ids = list(dict.fromkeys(
        #     t.station_id for t in tasks
        # ))

        scenario = Scenario(
            doc["scenario_id"],
            doc["type"],
            tasks
        )
        scenario.status = doc.get("status")
        return scenario
