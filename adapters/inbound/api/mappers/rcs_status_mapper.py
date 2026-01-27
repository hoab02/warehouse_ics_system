from domain.fsm.task_fsm import TaskStatus

class RcsStatusMapper:

    _MAP = {
        ("3", 8): TaskStatus.DONE,
        ("3", 10): TaskStatus.AT_STATION,
        ("2", 6): TaskStatus.RETURNING
    }

    @classmethod
    def to_domain(cls, sub_task_status: str, status: int) -> TaskStatus:
        try:
            return cls._MAP[(sub_task_status, status)]
        except KeyError:
            raise ValueError(
                f"Unknown RCS status: subTaskStatus={sub_task_status}, status={status}"
            )
