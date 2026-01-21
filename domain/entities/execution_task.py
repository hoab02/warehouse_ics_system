from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List, Optional
from domain.fsm.task_fsm import TaskStatus

@dataclass(frozen=True)
class CompletedPickingTask:
    picking_session_code: str
    picking_task_code: str
    or_code: str

# class ExecutionTask:
#     def __init__(self,
#                  base_sequence,
#                  scenario_id,
#                  station_id,
#                  shelf_id,
#                  actions,
#                  logical_task_ids):
#         self.base_sequence = base_sequence
#         self.station_id = station_id
#         self.shelf_id = shelf_id
#         self.actions = actions  # [Move & Rotate Shelf or not]
#         self.logical_task_ids = logical_task_ids
#         self.scenario_id = scenario_id
#         self.status = TaskStatus.PENDING

class ExecutionTask:
    def __init__(
        self,
        scenario_id: str,
        station_id: str,
        shelf_id: str,
        logical_task_ids: str,

        # optional / legacy
        base_sequence: Optional[int] = None,

        # NEW
        merged_picking_tasks: Optional[List[CompletedPickingTask]] = None,
        need_rotate: bool = False,
        target_side: Optional[str] = None,
    ):
        self.scenario_id = scenario_id
        self.station_id = station_id
        self.shelf_id = shelf_id

        self.logical_task_ids = logical_task_ids
        self.base_sequence = base_sequence

        # merge-related
        self.merged_picking_tasks = merged_picking_tasks or []
        self.need_rotate = need_rotate
        self.target_side = target_side

        # infra
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now(timezone.utc)
