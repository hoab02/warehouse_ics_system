from pydantic import BaseModel
from domain.entities.task import Task

class TaskDTO(BaseModel):
    sequence: int
    shelf_id: str
    station_id: str
    side: str

    def to_domain(self) -> Task:
        return Task(
            sequence=self.sequence,
            shelf_id=self.shelf_id,
            station_id=self.station_id,
            side=self.side
        )
