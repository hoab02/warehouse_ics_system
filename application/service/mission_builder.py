class MissionBuilder:
    """
    Build RCS mission payload from ExecutionTask (ModelProcessCode)
    """

    def __init__(self, callback_url: str):
        self.callback_url = callback_url

    def build(self, execution_task):

        return {
            "mission_id": execution_task.logical_task_ids,
            "scenario_id": execution_task.scenario_id,
            "type": "SHELF_OPERATION",
            "station_id": execution_task.station_id,
            "shelf_id": execution_task.shelf_id,
            "actions": [],
            "callback": {
                "url": self.callback_url,
                "method": "POST"
            }
        }

    def build_return_shelf_mission(self, mission):

        return {
            "mission_type": "RETURN_SHELF",
            "scenario_id": mission.scenario_id,
            "execution_task_id": mission.logical_task_ids,
            "shelf_id": mission.shelf_id,
            "from_station": mission.station_id,
        }
