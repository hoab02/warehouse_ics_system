import requests
from ports.outbound.wss_notifier_port import WssNotifierPort

class WssHttpNotifierAdapter(WssNotifierPort):

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def notify_execution_task(self, task_id: str, status: str):
        requests.post(
            f"{self.base_url}/execution-task/status",
            json={"task_id": task_id, "status": status}
        )

    def notify_scenario(self, scenario_id: str, status: str):
        requests.post(
            f"{self.base_url}/scenario/status",
            json={"scenario_id": scenario_id, "status": status}
        )
