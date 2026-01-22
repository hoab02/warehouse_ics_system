from abc import ABC, abstractmethod

class WssNotifierPort(ABC):

    @abstractmethod
    def notify_execution_task(self, mission: dict) -> None:
        pass

    @abstractmethod
    def notify_scenario(self, scenario_id: str, status: str) -> None:
        pass
