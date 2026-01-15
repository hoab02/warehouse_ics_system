from abc import ABC, abstractmethod


class ResourceLockPort(ABC):

    @abstractmethod
    def acquire(self, resource_type: str, resource_id: str,
                owner_id: str, scenario_id: str) -> bool:
        pass

    @abstractmethod
    def release(self, resource_type: str, resource_id: str) -> None:
        pass
