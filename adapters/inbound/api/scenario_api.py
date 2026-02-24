from fastapi import APIRouter, Depends, HTTPException, status, Response

from adapters.inbound.api.schemas import ScenarioPayload, CreateScenarioResponse
from application.dto.scenario_dto import ScenarioDTO
from application.dto.task_dto import TaskDTO
from application.use_cases.create_scenario import CreateScenarioUseCase
from ports.outbound.logger_port import LoggerPort
from common.log_context import LogContext
from domain.exceptions import (
    ScenarioAlreadyExistsException,
    ScenarioValidationException,
    InvalidTaskOrderError,
)

router = APIRouter()

def get_create_scenario_use_case():
    from main import create_scenario_use_case
    return create_scenario_use_case

def get_logger() -> LoggerPort:
    from main import logger
    return logger


@router.post(
    "",
    response_model=CreateScenarioResponse,
    status_code=201,
)
def create_scenario(
    payload: ScenarioPayload,
    response: Response,
    use_case: CreateScenarioUseCase = Depends(get_create_scenario_use_case),
    logger: LoggerPort = Depends(get_logger),
):
    context = LogContext(
        trace_id=payload.scenario_id,
        scenario_id=payload.scenario_id,
        task_id=None,
        source="API_CREATE_SCENARIO",
    )

    payload_dict = payload.model_dump()

    logger.info(
        event="API_CREATE_SCENARIO_REQUEST",
        context=context,
        fields={
            "message": payload_dict,
        },
    )

    try:
        task_dtos = [
            TaskDTO(
                sequence=t.sequence,
                picking_session_code=t.picking_session_code,
                picking_task_code=t.picking_task_code,
                or_code=t.or_code,
                shelf_id=t.shelf_code,
                station_id=t.station_code,
                side=t.side_code,
            )
            for t in payload.tasks
        ]

        scenario_dto = ScenarioDTO(
            scenario_id=payload.scenario_id,
            type=payload.type,
            tasks=task_dtos,
        )

        scenario_id = use_case.execute(scenario_dto)

        response.headers["Location"] = f"/scenarios/{scenario_id}"

        return CreateScenarioResponse(
            scenario_id=scenario_id,
            status="CREATED",
        )

    except ScenarioAlreadyExistsException as e:
        logger.warning(
            event="API_CREATE_SCENARIO_CONFLICT",
            context=context,
            fields={"reason": str(e)},
        )
        raise HTTPException(status_code=409, detail=str(e))

    except (ScenarioValidationException, InvalidTaskOrderError) as e:
        logger.warning(
            event="API_CREATE_SCENARIO_VALIDATION_FAILED",
            context=context,
            fields={"reason": str(e)},
        )
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        logger.error(
            event="API_CREATE_SCENARIO_UNEXPECTED_ERROR",
            context=context,
            exception=e,
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )