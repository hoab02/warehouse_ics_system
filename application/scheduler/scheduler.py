class Scheduler:
    def __init__(self, execution_task_repo, station_lock, rcs_mission_port, mission_builder):
        self.execution_task_repo = execution_task_repo
        self.station_lock = station_lock
        # self.shelf_lock = shelf_lock
        self.rcs_mission_port = rcs_mission_port
        self.builder = mission_builder


    def tick(self):
        for task in self.execution_task_repo.find_created():
            # if self.station_lock.try_lock(task.station_id, task.id) and \
            # self.shelf_lock.try_lock(task.shelf_id, task.id):
            by_task = f"{task.scenario_id}:{task.logical_task_ids}"
            if self.station_lock.try_lock(task.station_id, by_task):
                mission = self.builder.build(task)
                print("Hello")
                self.execution_task_repo.update_status(task.logical_task_ids, "DISPATCHED")
                self.rcs_mission_port.send_mission(mission)