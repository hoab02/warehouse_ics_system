from abc import ABC, abstractmethod


class LocationPort(ABC):

    @abstractmethod
    def get_shelf_point(self, shelf_id: str) -> str:
        """Return point code for a shelf"""
        pass

    @abstractmethod
    def get_station_point(self, station_id: str) -> str:
        """Return point code for a station"""
        pass