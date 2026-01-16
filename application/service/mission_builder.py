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