from ports.repositories.scenario_repository import ScenarioRepository
from adapters.outbound.mongo.mappers.scenario_mapper import ScenarioMapper
from adapters.outbound.mongo.collections import Collections


class ScenarioMongoRepository(ScenarioRepository):

    def __init__(self, db):
        self.col = db[Collections.SCENARIOS]


    def save(self, scenario):
        self.col.insert_one(ScenarioMapper.to_document(scenario))


    def get(self, scenario_id):
        doc = self.col.find_one({"_id": scenario_id})
        return ScenarioMapper.from_document(doc) if doc else None


    def update_status(self, scenario_id, status):
        self.col.update_one(
        {"_id": scenario_id},
        {"$set": {"status": status}}
        )