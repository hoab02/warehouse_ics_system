from domain.entities.execution_task import ExecutionTask

class ExecutionTaskMapper:

    @staticmethod
    def to_document(t: ExecutionTask) -> dict:
        return {
                "base_sequence": t.base_sequence,
                "logical_task_ids": t.logical_task_ids,
                "scenario_id": t.scenario_id,
                "station_id": t.station_id,
                "shelf_id": t.shelf_id,
                "actions": t.actions,
                "status": t.status
        }


    @staticmethod
    def from_document(doc: dict) -> ExecutionTask:
        task = ExecutionTask(
            doc["base_sequence"],
            doc["scenario_id"],
            doc["station_id"],
            doc["shelf_id"],
            doc["actions"],
            doc["logical_task_ids"]
        )
        task.status = doc["status"]
        return task