from dataclasses import dataclass
from domain.fsm.task_fsm import TaskStatus

@dataclass(frozen=True)
class RcsCallbackCommand:
    mission_id: str
    status: TaskStatus


class RcsCallbackHandler:

    def __init__(self, execution_task_repo, scenario_repo, resource_lock, status_notifier):
        self.execution_task_repo = execution_task_repo
        self.scenario_repo = scenario_repo
        self.resource_lock = resource_lock
        self.status_notifier = status_notifier

        self._handlers = {
            TaskStatus.DONE: self._on_completed,
            TaskStatus.FAILED: self._on_failed,
            TaskStatus.MOVING: self._on_moving,
        }

    def handle(self, command: RcsCallbackCommand):
        task = self.execution_task_repo.get(command.mission_id)

        if not task:
            raise ValueError(f"Unknown mission_id {command.mission_id}")

        try:
            handler = self._handlers[command.status]
        except KeyError:
            raise ValueError(f"Unsupported status: {command.status}")

        handler(task, command)

    def _update_and_notify(self, task, status: TaskStatus):
        self.execution_task_repo.update_status(task.logical_task_ids, status)
        self.status_notifier.notify_execution_task(task.logical_task_ids, status)

    def _on_completed(self, task, command):
        print(f"Mission {command.mission_id} completed")
        self._update_and_notify(task, command.status)
        self._post_update(task)

    def _on_failed(self, task, command):
        print(f"Mission {command.mission_id} failed")
        self._update_and_notify(task, command.status)
        self._post_update(task)

    def _on_moving(self, task, command):
        print(f"Mission {command.mission_id} running")
        self._update_and_notify(task, command.status)

    def _post_update(self, task):
        # Release locks
        self.resource_lock.release("station", task.station_id)
        self.resource_lock.release("shelf", task.shelf_id)

        # Recompute scenario
        tasks = self.execution_task_repo.get_by_scenario(task.scenario_id)
        new_status = self._compute_scenario_status(tasks)

        scenario = self.scenario_repo.get(task.scenario_id)
        if scenario.status != new_status:
            self.scenario_repo.update_status(task.scenario_id, new_status)
            self.status_notifier.notify_scenario(task.scenario_id, new_status)

    @staticmethod
    def _compute_scenario_status(tasks):
        statuses = {t.status for t in tasks}

        if TaskStatus.FAILED in statuses:
            return TaskStatus.FAILED
        if statuses == {TaskStatus.DONE}:
            return TaskStatus.DONE
        if statuses & {TaskStatus.MOVING, TaskStatus.DISPATCHED}:
            return TaskStatus.MOVING

        return TaskStatus.DISPATCHED