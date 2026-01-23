from fastapi import APIRouter, Depends
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
    print("Hello")
    station_id = payload.station_code
    use_case.execute_return(station_id)
    return {"status": "RETURN_TRIGGERED"}
