class RcsCallbackHandler:

    TERMINAL_STATUSES = {"DONE", "FAILED"}

    def __init__(self, execution_task_repo, scenario_repo, resource_lock, status_notifier):
        self.execution_task_repo = execution_task_repo
        self.scenario_repo = scenario_repo
        self.resource_lock = resource_lock
        self.status_notifier = status_notifier


    def handle(self, mission_id: str, status: str):
        task = self.execution_task_repo.get(mission_id)
        if not task:
            raise ValueError(f"Unknown mission_id {mission_id}")

        # Idempotency guard
        if task.status in self.TERMINAL_STATUSES:
            return

        # Update execution task status
        self.execution_task_repo.update_status(task.logical_task_ids, status)
        # self.status_notifier.notify_execution_task(task.logical_task_ids, status)

        # Release locks if terminal
        if status in self.TERMINAL_STATUSES:
            self.resource_lock.release("station", task.station_id)
            self.resource_lock.release("shelf", task.shelf_id)

        # Recompute scenario status
        tasks = self.execution_task_repo.get_by_scenario(task.scenario_id)
        new_scenario_status = self._compute_scenario_status(tasks)
        scenario = self.scenario_repo.get(task.scenario_id)

        # Update scenario if changed
        if scenario.status != new_scenario_status:
            self.scenario_repo.update_status(
                task.scenario_id, new_scenario_status
            )
            self.status_notifier.notify_scenario(
                task.scenario_id, new_scenario_status
            )

    @staticmethod
    def _compute_scenario_status(tasks):
        statuses = [t.status for t in tasks]

        if any(s == "FAILED" for s in statuses):
            return "FAILED"
        if all(s == "DONE" for s in statuses):
            return "DONE"
        if any(s in ("RUNNING", "DISPATCHED") for s in statuses):
            return "RUNNING"

        return "CREATED"