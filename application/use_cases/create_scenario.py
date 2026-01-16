# app/application/create_scenario.py
from domain.entities.scenario import Scenario
from domain.entities.task import Task, Side
from domain.validators.scenario_validator import validate_scenario_tasks
from domain.mergers.task_merger import merge_tasks

class CreateScenarioUseCase:

    def __init__(
        self,
        scenario_repo,
        execution_task_repo
    ):
        self.scenario_repo = scenario_repo
        self.execution_task_repo = execution_task_repo

    def execute(self, scenario_dto):
        existing = self.scenario_repo.get(scenario_dto.scenario_id)
        if existing:
            return existing.scenario_id
        validate_scenario_tasks(scenario_dto.tasks)
        tasks = []
        for idx, t in enumerate(scenario_dto.tasks):
            tasks.append(
                Task(
                    sequence=t.sequence,
                    shelf_id=t.shelf_id,
                    station_id=t.station_id,
                    side=Side(t.side),
                )
            )

        scenario = Scenario(
            scenario_id=scenario_dto.scenario_id,
            scenario_type = scenario_dto.type,
            tasks=tasks,
            stations=scenario_dto.stations
        )
        self.scenario_repo.save(scenario)

        execution_tasks = merge_tasks(scenario.scenario_id, scenario.tasks)
        for execution_task in execution_tasks:
            self.execution_task_repo.save(execution_task)

        return scenario.scenario_id