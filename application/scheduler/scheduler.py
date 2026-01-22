class Scheduler:

    def __init__(
        self,
        scenario_repo,
        execution_task_repo,
        resource_lock,
        rcs_mission_port,
        mission_builder
    ):
        self.scenario_repo = scenario_repo
        self.execution_task_repo = execution_task_repo
        self.lock = resource_lock
        self.rcs = rcs_mission_port
        self.builder = mission_builder

    def tick(self):
        scenario = self.scenario_repo.get_running()

        if not scenario:
            # nếu chưa có → lấy scenario kế
            scenario = self.scenario_repo.get_next_queued()
            if not scenario:
                return

            self.scenario_repo.update_status(
                scenario.scenario_id, "RUNNING"
            )

        # chỉ lấy task của scenario này
        tasks = self.execution_task_repo.find_created_by_scenario(
            scenario.scenario_id
        )

        for task in tasks:
            # lock station
            if not self.lock.acquire(
                    "station",
                    task.station_id,
                    task.logical_task_ids,
                    task.scenario_id
            ):
                continue

            # lock shelf
            if not self.lock.acquire(
                    "shelf",
                    task.shelf_id,
                    task.logical_task_ids,
                    task.scenario_id
            ):
                self.lock.release("station", task.station_id)
                continue

            try:
                # build mission
                mission = self.builder.build(task)

                # send to RCS
                self.rcs.send_mission(
                    mission=mission,
                    idempotency_key=task.logical_task_ids
                )

                # update task status
                self.execution_task_repo.update_status(
                    task.logical_task_ids,
                    "DISPATCHED"
                )

            except Exception as e:
                # rollback
                self.lock.release("station", task.station_id)
                self.lock.release("shelf", task.shelf_id)
                raise e

