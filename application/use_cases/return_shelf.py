from domain.fsm.task_fsm import TaskStatus


class ReturnShelfUseCase:

    def __init__(self, execution_task_repo, rcs_mission_port, mission_builder):
        self.execution_task_repo = execution_task_repo
        self.rcs = rcs_mission_port
        self.builder = mission_builder

    def execute_return(self, logical_task_ids: str):
        task = self.execution_task_repo.get(logical_task_ids)

        if not task:
            raise ValueError("ExecutionTask not found")

        if task.status != TaskStatus.AT_STATION:
            raise ValueError(
                f"Task not ready for return, status={task.status}"
            )

        self.execution_task_repo.update_status(
            logical_task_ids,
            TaskStatus.WAITING_RETURN
        ) # tránh race condition

        mission = self.builder.build_return_shelf_mission(task)

        # send return mission
        self.rcs.send_return_mission(mission)
