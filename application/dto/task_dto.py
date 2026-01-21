from pydantic import BaseModel
from domain.entities.task import Task

# class TaskDTO(BaseModel):
#     sequence: int
#     shelf_id: str
#     station_id: str
#     side: str
#
#     def to_domain(self) -> Task:
#         return Task(
#             sequence=self.sequence,
#             shelf_id=self.shelf_id,
#             station_id=self.station_id,
#             side=self.side
#         )

class TaskDTO(BaseModel):
    sequence: int
    picking_session_code: str
    picking_task_code: str
    or_code: str
    shelf_id: str
    station_id: str
    side: str

    def to_domain(self) -> Task:
        return Task(
            sequence=self.sequence,
            picking_task_code=self.picking_task_code,
            picking_session_code=self.picking_session_code,
            or_code=self.or_code,
            shelf_id=self.shelf_id,
            station_id=self.station_id,
            side=self.side
        )