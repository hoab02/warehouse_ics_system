from domain.fsm.task_fsm import TaskStatus, validate_transition

class ExecutionTask:
    def __init__(self, base_sequence, scenario_id, station_id, shelf_id, actions, logical_task_ids):
        self.base_sequence = base_sequence
        self.station_id = station_id
        self.shelf_id = shelf_id
        self.actions = actions  # [Move & Rotate Shelf or not]
        self.logical_task_ids = logical_task_ids
        self.scenario_id = scenario_id
        self.status = TaskStatus.PENDING