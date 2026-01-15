import requests
from ports.outbound.rcs_mission_port import RcsMissionPort

class RcsHttpMissionAdapter(RcsMissionPort):

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def send_mission(self, mission: dict) -> None:
        resp = requests.post(
            f"{self.base_url}/missions",
            json=mission,
            headers={
                "Idempotency-Key": mission["mission_id"]
            },
            timeout=5
        )

        if resp.status_code not in (200, 201, 202):
            raise RuntimeError(
                f"RCS error {resp.status_code}: {resp.text}"
            )
