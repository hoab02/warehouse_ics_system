from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.return_shelf import ReturnShelfUseCase
from adapters.inbound.api.schemas import ReturnShelfPayload, ReturnShelfResponse
from ports.outbound.logger_port import LoggerPort
from common.log_context import LogContext

router = APIRouter()

def get_return_shelf_use_case():
    from main import return_shelf_use_cases
    return return_shelf_use_cases

def get_logger() -> LoggerPort:
    from main import logger
    return logger

@router.post(
    "",
    response_model=ReturnShelfResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Trigger return shelf process",
    description="Triggers a return shelf process for a given scenario and station."
)
def return_shelf(
    payload: ReturnShelfPayload,
    use_case: ReturnShelfUseCase = Depends(get_return_shelf_use_case),
    logger: LoggerPort = Depends(get_logger),
):
    context = LogContext(
        trace_id=payload.scenario_id,
        scenario_id=payload.scenario_id,
        task_id=None,
        source="API_RETURN_SHELF",
    )
    payload_dict = payload.model_dump()
    logger.info(
        event="API_RETURN_SHELF_REQUEST",
        context=context,
        fields={
            "message": payload_dict,
        },
    )

    try:

        station_id = payload.station_code
        scenario_id = payload.scenario_id
        use_case.execute_return(station_id, scenario_id)

        return ReturnShelfResponse(
            status="RETURN_SHELF_TRIGGERED",
            scenario_id=scenario_id,
            station_id=station_id,
        )

    except Exception as e:
        logger.error(
            event="API_RETURN_SHELF_UNEXPECTED_ERROR",
            context=context,
            fields={"reason": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
