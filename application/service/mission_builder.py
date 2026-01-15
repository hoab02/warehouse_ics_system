class MissionBuilder:
    """
    Build RCS mission payload from ExecutionTask (ModelProcessCode)
    """

    def __init__(self, callback_url: str):
        self.callback_url = callback_url

    def build(self, execution_task):
        return {
            "mission_id": execution_task.id,
            "scenario_id": execution_task.scenario_id,
            "type": "SHELF_OPERATION",
            "station_id": execution_task.station_id,
            "shelf_id": execution_task.shelf_id,
            "actions": [
                {"type": "MOVE_SHELF_TO_STATION", "station_id": execution_task.station_id},
                {"type": "ROTATE_SHELF", "side": execution_task.side}
            ],
            "callback": {
                "url": self.callback_url,
                "method": "POST"
            }
        }