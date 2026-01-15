from abc import ABC, abstractmethod

class ShelfLockRepository(ABC):

    @abstractmethod
    def try_lock(self, shelf_id: str, by_task: str) -> bool:
        pass

    @abstractmethod
    def release(self, shelf_id: str) -> None:
        pass
