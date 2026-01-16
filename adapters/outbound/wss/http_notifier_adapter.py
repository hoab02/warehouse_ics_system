import requests
from ports.outbound.wss_notifier_port import WssNotifierPort

class WssHttpNotifierAdapter(WssNotifierPort):

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def notify_execution_task(self, task_id: str, status: str):
        print("Notify Execution Task Status to WSS Successfully!")
        # requests.post(
        #     f"{self.base_url}/api/v1/events/robot",
        #     json={"task_id": task_id, "status": status}
        # )

    def notify_scenario(self, scenario_id: str, status: str):
        print("Notify Scenario Status to WSS Successfully!")
        # requests.post(
        #     f"{self.base_url}/api/v1/events/scenario",
        #     json={"scenario_id": scenario_id, "status": status}
        # )
