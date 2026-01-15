from abc import ABC, abstractmethod

class StationLockRepository(ABC):

    @abstractmethod
    def try_lock(self, station_id: str, by_task: str) -> bool:
        pass

    @abstractmethod
    def release(self, station_id: str) -> None:
        pass
