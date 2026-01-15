from datetime import datetime
from pymongo.errors import DuplicateKeyError
from ports.repositories.resource_lock_port import ResourceLockPort


class MongoResourceLockRepository(ResourceLockPort):

    def __init__(self, db):
        self.col = db["resource_locks"]

    def acquire(self, resource_type, resource_id, owner_id, scenario_id) -> bool:
        try:
            self.col.insert_one({
                "_id": f"{resource_type}:{resource_id}",
                "resource_type": resource_type,
                "resource_id": resource_id,
                "locked_by": owner_id,
                "scenario_id": scenario_id,
                "created_at": datetime.utcnow()
            })
            return True
        except DuplicateKeyError:
            return False

    def release(self, resource_type, resource_id):
        self.col.delete_one({
            "_id": f"{resource_type}:{resource_id}"
        })
