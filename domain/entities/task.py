from enum import Enum

class Side(str, Enum):
    FRONT = "FRONT"
    BACK = "BACK"

    @classmethod
    def validate(cls, value):
        if value not in (cls.FRONT, cls.BACK):
            raise ValueError(f"Invalid side: {value}")


class Task:
    def __init__(self,
                 sequence: int,
                 shelf_id: str,
                 side: str,
                 station_id: str,
                 picking_session_code: str,
                 picking_task_code: str,
                 or_code: str
                 ):
        self.sequence = sequence
        self.shelf_id = shelf_id
        self.side = side
        self.station_id = station_id
        self.picking_session_code = picking_session_code
        self.picking_task_code = picking_task_code
        self.or_code = or_code
