from typing import List

from domain.entities.execution_task import ExecutionTask
from ports.repositories.execution_task_repository import ExecutionTaskRepository
from adapters.outbound.mongo.mappers.execution_task_mapper import ExecutionTaskMapper
from adapters.outbound.mongo.collections import Collections


class ExecutionTaskMongoRepository(ExecutionTaskRepository):


    def __init__(self, db):
        self.col = db[Collections.EXECUTION_TASKS]


    def save(self, task):
        self.col.insert_one(ExecutionTaskMapper.to_document(task))

    def find_created(self):
        docs = self.col.find({"status": "PENDING"})
        return [ExecutionTaskMapper.from_document(d) for d in docs]


    def get(self, task_id):
        doc = self.col.find_one({"logical_task_ids": task_id})
        return ExecutionTaskMapper.from_document(doc) if doc else None

    def get_by_scenario(self, scenario_id) -> list[ExecutionTask]:
        """
        Return ALL execution tasks for a scenario.
        Used by callback to recompute scenario status.
        """
        cursor = self.col.find(
            {"scenario_id": scenario_id}
        )

        return [
            ExecutionTaskMapper.from_document(doc)
            for doc in cursor
        ]

    def update_status(self, task_id, status):
        self.col.update_one(
        {"logical_task_ids": task_id},
        {"$set": {"status": status}}
        )


    def find_created_by_scenario(
            self, scenario_id: str
    ) -> list[ExecutionTask]:
        cursor = self.col.find(
            {
                "scenario_id": scenario_id,
                "status": "PENDING"
            }
        ).sort("base_sequence", 1)
        return [ExecutionTaskMapper.from_document(d) for d in cursor]
