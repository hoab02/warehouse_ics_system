from abc import ABC, abstractmethod
from domain.entities.execution_task import ExecutionTask
from typing import Optional

class ExecutionTaskRepository(ABC):

    @abstractmethod
    def save(self, task: ExecutionTask) -> None:
        pass

    @abstractmethod
    def find_created(self) -> list[ExecutionTask]:
        pass

    @abstractmethod
    def get(self, task_id: str) -> Optional[ExecutionTask]:
        pass

    @abstractmethod
    def get_by_scenario(self, scenario_id) -> list[ExecutionTask]:
        pass

    @abstractmethod
    def update_status(self, task_id: str, status: str) -> None:
        pass

    @abstractmethod
    def find_created_by_scenario(
            self, scenario_id: str
    ) -> list[ExecutionTask]:
        pass
