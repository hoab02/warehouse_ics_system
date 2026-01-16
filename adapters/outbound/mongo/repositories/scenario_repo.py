from pymongo.errors import DuplicateKeyError
from ports.repositories.scenario_repository import ScenarioRepository
from adapters.outbound.mongo.mappers.scenario_mapper import ScenarioMapper
from adapters.outbound.mongo.collections import Collections


class ScenarioMongoRepository(ScenarioRepository):

    def __init__(self, db):
        self.col = db[Collections.SCENARIOS]
        self.col.create_index(
            [("scenario_id", 1)],
            unique=True
        )

    def get_running(self):
        doc = self.col.find_one(
            {"status": "RUNNING"}
        )

        if not doc:
            return None

        return ScenarioMapper.from_document(doc)

    def get_next_queued(self):
        doc = self.col.find_one(
            {"status": "CREATE"},
            sort=[("created_at", 1)]
        )

        if not doc:
            return None

        return ScenarioMapper.from_document(doc)


    def save(self, scenario):
        try:
            self.col.insert_one(ScenarioMapper.to_document(scenario))
        except DuplicateKeyError:
            # Idempotent behavior → ignore or rethrow business error
            pass

    def get(self, scenario_id):
        doc = self.col.find_one({"scenario_id": scenario_id})
        return ScenarioMapper.from_document(doc) if doc else None


    def update_status(self, scenario_id, status):
        self.col.update_one(
        {"scenario_id": scenario_id},
        {"$set": {"status": status}}
        )