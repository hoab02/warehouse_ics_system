from fastapi import APIRouter, Depends, HTTPException, status

from adapters.inbound.api.schemas import ScenarioPayload
from application.dto.scenario_dto import ScenarioDTO
from application.dto.task_dto import TaskDTO
from application.use_cases.create_scenario import CreateScenarioUseCase
from domain.exceptions import ScenarioAlreadyExistsException, ScenarioValidationException, InvalidTaskOrderError
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

def get_create_scenario_use_case():
    from main import create_scenario_use_case
    return create_scenario_use_case

@router.post("")
def create_scenario(
    payload: ScenarioPayload,
    use_case: CreateScenarioUseCase = Depends(get_create_scenario_use_case)
):
    logger.info("CREATE SCENARIO API CALLED")
    try:
        task_dtos = [
            TaskDTO(
                sequence=t.sequence,
                picking_session_code=t.picking_session_code,
                picking_task_code=t.picking_task_code,
                or_code=t.or_code,
                shelf_id=t.shelf_code,
                station_id=t.station_code,
                side=t.side_code
            )
            for t in payload.tasks
        ]

        scenario_dto = ScenarioDTO(
            scenario_id=payload.scenario_id,
            type=payload.type,
            tasks=task_dtos
        )
        scenario_id = use_case.execute(scenario_dto)
        return {"scenario_id": scenario_id, "status": "CREATED"}

    except ScenarioAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except ScenarioValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except InvalidTaskOrderError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
