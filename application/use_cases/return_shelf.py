from domain.fsm.task_fsm import TaskStatus


class ReturnShelfUseCase:

    def __init__(self, execution_task_repo, rcs_mission_port, mission_builder):
        self.execution_task_repo = execution_task_repo
        self.rcs = rcs_mission_port
        self.builder = mission_builder

    def execute_return(self, station_id: str):
        task = self.execution_task_repo.get_active_by_station(station_id)

        if not task:
            raise ValueError("ExecutionTask not found")

        self.execution_task_repo.update_status(
            task.logical_task_ids,
            TaskStatus.WAITING_RETURN
        ) # avoid race condition

        mission = self.builder.build_return_shelf_mission(task)

        # send return mission
        self.rcs.send_return_mission(mission, task.logical_task_ids)
