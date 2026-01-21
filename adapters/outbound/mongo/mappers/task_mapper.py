from domain.entities.task import Task

class TaskMapper:
    @staticmethod
    def to_document(task: Task):
        return {
            "sequence": task.sequence,
            "shelf_id": task.shelf_id,
            "station_id": task.station_id,
            "side": task.side,
            "picking_session_code": task.picking_session_code,
            "picking_task_code": task.picking_task_code,
            "or_code": task.or_code
        }

    @staticmethod
    def from_document(doc: dict) -> Task:
        return Task(
            sequence=doc["sequence"],
            shelf_id=doc["shelf_id"],
            station_id=doc["station_id"],
            side=doc["side"],
            picking_task_code=doc["picking_task_code"],
            picking_session_code=doc["picking_session_code"],
            or_code=doc["or_code"]
        )