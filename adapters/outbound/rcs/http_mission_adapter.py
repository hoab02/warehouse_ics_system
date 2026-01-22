import requests
from ports.outbound.rcs_mission_port import RcsMissionPort

class RcsHttpMissionAdapter(RcsMissionPort):

    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def send_mission(self, mission: dict, idempotency_key: str) -> None:
        resp = requests.post(
            f"{self.base_url}/ics/taskOrder/addTask",
            json=mission,
            headers={
                "Idempotency-Key": idempotency_key
            },
            timeout=self.timeout
        )

        if resp.status_code not in (200, 201, 202):
            raise RuntimeError(
                f"RCS error {resp.status_code}: {resp.text}"
            )

    def send_return_mission(self, mission: dict) -> None:
        print("Sent return mission successfully!")

        # resp = requests.post(
        #     f"{self.base_url}/return_shelf",
        #     json=mission,
        #     headers={
        #         "Idempotency-Key": mission["mission_id"]
        #     },
        #     timeout=5
        # )
        #
        # if resp.status_code not in (200, 201, 202):
        #     raise RuntimeError(
        #         f"RCS error {resp.status_code}: {resp.text}"
        #     )
