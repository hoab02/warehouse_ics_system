import json
from ports.outbound.location_port import LocationPort


class JsonLocationAdapter(LocationPort):

    def __init__(self, config_path: str):
        self._data = self._load_config(config_path)

    def _load_config(self, path: str) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            warehouse = raw["warehouse"]
            default_wh = warehouse["default_warehouse"]
            return warehouse["warehouses"][default_wh]

        except FileNotFoundError:
            raise RuntimeError(f"Location config file not found: {path}")
        except KeyError as e:
            raise RuntimeError(f"Invalid location config structure, missing {e}")

    # ---------- Port implementations ----------

    def get_shelf_point(self, shelf_id: str) -> str:
        try:
            return self._data["shelves"][shelf_id]["point"]
        except KeyError:
            raise RuntimeError(f"Shelf point not found: {shelf_id}")


    def get_station_point(self, station_id: str) -> str:
        try:
            return self._data["stations"][station_id]["point"]
        except KeyError:
            raise RuntimeError(f"Station point not found: {station_id}")
