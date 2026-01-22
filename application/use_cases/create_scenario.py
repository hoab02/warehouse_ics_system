from domain.entities.scenario import Scenario
from domain.entities.task import Task, Side
from domain.exceptions import ScenarioAlreadyExistsException
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
            raise ScenarioAlreadyExistsException(
                f"Scenario {scenario_dto.scenario_id} already exists"
            )

        validate_scenario_tasks(scenario_dto.tasks)

        tasks = []
        for idx, t in enumerate(scenario_dto.tasks):
            tasks.append(
                Task(
                    sequence=t.sequence,
                    picking_task_code=t.picking_task_code,
                    picking_session_code=t.picking_session_code,
                    or_code=t.or_code,
                    shelf_id=t.shelf_id,
                    station_id=t.station_id,
                    side=t.side
                )
            )

        scenario = Scenario(
            scenario_id=scenario_dto.scenario_id,
            scenario_type = scenario_dto.type,
            tasks=tasks
        )
        self.scenario_repo.save(scenario)

        execution_tasks = merge_tasks(scenario.scenario_id, scenario.tasks)
        for execution_task in execution_tasks:
            self.execution_task_repo.save(execution_task)

        return scenario.scenario_id