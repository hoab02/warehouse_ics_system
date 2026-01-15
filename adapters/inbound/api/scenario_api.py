from fastapi import APIRouter, Depends
from adapters.inbound.api.schemas import ScenarioPayload
from application.dto.scenario_dto import ScenarioDTO
from application.dto.task_dto import TaskDTO
from application.use_cases.create_scenario import CreateScenarioUseCase

router = APIRouter()

def get_create_scenario_use_case():
    from main import create_scenario_use_case
    return create_scenario_use_case

@router.post("")
def create_scenario(
    payload: ScenarioPayload,
    use_case: CreateScenarioUseCase = Depends(get_create_scenario_use_case)
):
    task_dtos = [
        TaskDTO(
            sequence=t.sequence,
            shelf_id=t.shelf_id,
            station_id=t.station_id,
            side=t.side
        )
        for t in payload.tasks
    ]

    scenario_dto = ScenarioDTO(
        scenario_id=payload.scenario_id,
        type=payload.type,
        stations=payload.stations,
        tasks=task_dtos
    )
    scenario_id = use_case.execute(scenario_dto)
    return {"scenario_id": scenario_id, "status": "CREATED"}
