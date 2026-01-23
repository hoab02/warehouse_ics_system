from domain.entities.execution_task import ExecutionTask
from application.service.location_service import LocationService

class MissionBuilder:
    """
    Build RCS mission payload from ExecutionTask
    """

    def __init__(
        self,
        location_service: LocationService,
    ):
        self._location_service = location_service

    def build(self, execution_task: ExecutionTask) -> dict:
        from_point = self._location_service.resolve_shelf_point(
            execution_task.shelf_id
        )

        to_point = self._location_service.resolve_station_point(
            execution_task.station_id
        )

        return {
            "modelProcessCode": "chuku",
            "priority": 6,
            "fromSystem": "MES",
            "orderId": execution_task.logical_task_ids,
            "taskOrderDetail": [
                {
                    "taskPath": f"{from_point},{to_point}",
                    "shelfNumber": f"{execution_task.shelf_id}"
                }
            ]
        }

    def build_return_shelf_mission(self, mission):
        return {
            "orderId": mission.logical_task_ids
        }

    def build_callback_payload(self, execution_task: ExecutionTask) -> dict:
        return {
            "scenario_id": execution_task.scenario_id,
            "shelf_code": execution_task.shelf_id,
            "station_code": execution_task.station_id,
            "data": [
                {
                    "picking_session_code": t.picking_session_code,
                    "picking_task_code": t.picking_task_code,
                    "or_code": t.or_code,
                }
                for t in execution_task.merged_picking_tasks
            ],
        }

