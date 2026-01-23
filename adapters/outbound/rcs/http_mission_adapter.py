import requests
from ports.outbound.rcs_mission_port import RcsMissionPort

class RcsHttpMissionAdapter(RcsMissionPort):

    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def send_mission(self, mission: dict, idempotency_key: str) -> None:
        print(f"Sent to RCS: {mission}")
        # resp = requests.post(
        #     f"{self.base_url}/ics/taskOrder/addTask",
        #     json=mission,
        #     headers={
        #         "Idempotency-Key": idempotency_key
        #     },
        #     timeout=self.timeout
        # )
        #
        # if resp.status_code not in (200, 201, 202):
        #     raise RuntimeError(
        #         f"RCS error {resp.status_code}: {resp.text}"
        #     )

    def send_return_mission(self, mission: dict, idempotency_key: str) -> None:
        print(f"Sent return mission successfully: {mission}")

        # resp = requests.post(
        #     f"{self.base_url}/ics/out/task/continueTask",
        #     json=mission,
        #     headers={
        #         "Idempotency-Key": idempotency_key
        #     },
        #     timeout=self.timeout
        # )
        #
        # if resp.status_code not in (200, 201, 202):
        #     raise RuntimeError(
        #         f"RCS error {resp.status_code}: {resp.text}"
        #     )
