from abc import ABC, abstractmethod

class RcsMissionPort(ABC):

    @abstractmethod
    def send_mission(self, mission: dict) -> None:
        """Idempotent by mission_id"""
        pass
