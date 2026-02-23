from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.return_shelf import ReturnShelfUseCase
from adapters.inbound.api.schemas import ReturnShelfPayload

router = APIRouter()

def get_return_shelf_use_case():
    from main import return_shelf_use_cases
    return return_shelf_use_cases

# @router.post("/{logical_task_ids}/return")
@router.post("")
def return_shelf(
    payload: ReturnShelfPayload,
    use_case: ReturnShelfUseCase = Depends(get_return_shelf_use_case),
):
    try:
        station_id = payload.station_code
        scenario_id = payload.scenario_id
        use_case.execute_return(station_id, scenario_id)
        return {"status": "RETURN_TRIGGERED"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
