from ports.repositories.station_lock_repository import StationLockRepository
from datetime import datetime
from adapters.outbound.mongo.collections import Collections


class StationLockMongoRepository(StationLockRepository):


    def __init__(self, db):
        self.col = db[Collections.STATION_LOCKS]

    def try_lock(self, station_id, by_task):
        result = self.col.update_one(
            {
                "station_id": station_id,
                "locked_by": None
            },
            {
                "$set": {
                    "locked_by": by_task,
                    "locked_at": datetime.utcnow()
                }
            },
            upsert=True
        )
        return result.modified_count == 1 or result.upserted_id is not None

    def release(self, station_id):
        self.col.update_one(
        {"station_id": station_id},
        {"$set": {"locked_by": None, "locked_at": None}}
        )