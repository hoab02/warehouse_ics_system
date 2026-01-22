from adapters.outbound.mongo.mappers.completed_picking_task_mapper import CompletedPickingTaskMapper
from domain.entities.execution_task import ExecutionTask
from domain.fsm.task_fsm import TaskStatus


class ExecutionTaskMapper:

    @staticmethod
    def to_document(t: ExecutionTask) -> dict:
        return {
                "base_sequence": t.base_sequence,
                "logical_task_ids": t.logical_task_ids,
                "scenario_id": t.scenario_id,
                "station_id": t.station_id,
                "shelf_id": t.shelf_id,

                "merged_picking_tasks": [
                CompletedPickingTaskMapper.to_dict(x)
                for x in t.merged_picking_tasks
            ],

                "need_rotate": t.need_rotate,
                "target_side": t.target_side,
                "status": t.status,
                "created_at": t.created_at
        }


    @staticmethod
    def from_document(doc: dict) -> ExecutionTask:
        task = ExecutionTask(
            scenario_id=doc["scenario_id"],
            station_id=doc["station_id"],
            shelf_id=doc["shelf_id"],
            logical_task_ids=doc["logical_task_ids"],
            base_sequence=doc.get("base_sequence"),
            merged_picking_tasks=[
                CompletedPickingTaskMapper.from_dict(x)
                for x in doc.get("merged_picking_tasks", [])
            ],
            need_rotate=doc.get("need_rotate", False),
            target_side=doc.get("target_side"),
        )

        task.status = TaskStatus(doc["status"])
        task.created_at = doc["created_at"]

        return task
