from domain.fsm.task_fsm import TaskStatus, validate_transition

class ExecutionTask:
    def __init__(self, scenario_id, station_id, shelf_id, actions, logical_task_ids):
        self.station_id = station_id
        self.shelf_id = shelf_id
        self.actions = actions  # [Move & Rotate Shelf or not]
        self.logical_task_ids = logical_task_ids
        self.scenario_id = scenario_id
        self.status = TaskStatus.PENDING

    def move(self):
        validate_transition(self.status, TaskStatus.MOVING)
        self.status = TaskStatus.MOVING

    def arrive_station(self):
        validate_transition(self.status, TaskStatus.AT_STATION)
        self.status = TaskStatus.AT_STATION

    def wait_return(self):
        validate_transition(self.status, TaskStatus.WAITING_RETURN)
        self.status = TaskStatus.WAITING_RETURN

    def complete(self):
        validate_transition(self.status, TaskStatus.DONE)
        self.status = TaskStatus.DONE