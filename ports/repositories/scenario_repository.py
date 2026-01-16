from abc import ABC, abstractmethod
from domain.entities.scenario import Scenario
from typing import Optional

class ScenarioRepository(ABC):

    @abstractmethod
    def save(self, scenario: Scenario) -> None:
        pass

    @abstractmethod
    def get(self, scenario_id: str) -> Optional[Scenario]:
        pass

    @abstractmethod
    def update_status(self, scenario_id: str, status: str) -> None:
        pass

    @abstractmethod
    def get_running(self) -> Optional[Scenario]:
        pass

    @abstractmethod
    def get_next_queued(self) -> Optional[Scenario]:
        pass