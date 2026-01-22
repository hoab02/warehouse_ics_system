from ports.outbound.location_port import LocationPort


class LocationService:
    """
    Domain service responsible for resolving business IDs
    (shelf_id, station_id) to physical points in warehouse.
    """

    def __init__(self, location_port: LocationPort):
        self._location_port = location_port

    def resolve_shelf_point(self, shelf_id: str) -> str:
        """
        Resolve shelf_id to main shelf point.
        """
        return self._location_port.get_shelf_point(shelf_id)

    def resolve_station_point(self, station_id: str) -> str:
        """
        Resolve station_id to station point.
        """
        return self._location_port.get_station_point(station_id)