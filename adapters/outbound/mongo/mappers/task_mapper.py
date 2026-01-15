from domain.entities.task import Task

class TaskMapper:
    @staticmethod
    def to_document(task: Task):
        return {
            "sequence": task.sequence,
            "shelf_id": task.shelf_id,
            "station_id": task.station_id,
            "side": task.side
        }
