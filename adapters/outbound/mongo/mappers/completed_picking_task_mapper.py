from domain.entities.execution_task import CompletedPickingTask

class CompletedPickingTaskMapper:

    @staticmethod
    def to_dict(t: CompletedPickingTask) -> dict:
        return {
            "picking_session_code": t.picking_session_code,
            "picking_task_code": t.picking_task_code,
            "or_code": t.or_code,
        }

    @staticmethod
    def from_dict(d: dict) -> CompletedPickingTask:
        return CompletedPickingTask(
            picking_session_code=d["picking_session_code"],
            picking_task_code=d["picking_task_code"],
            or_code=d["or_code"],
        )
