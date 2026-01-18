from fastapi import APIRouter, Depends
from application.use_cases.return_shelf import ReturnShelfUseCase
from adapters.inbound.api.schemas import ReturnShelfPayload

router = APIRouter()

def get_return_shelf_use_case():
    from main import return_shelf_use_cases
    return return_shelf_use_cases

# @router.post("/{logical_task_ids}/return")
@router.post("/return")
def return_shelf(
    payload: ReturnShelfPayload,
    use_case: ReturnShelfUseCase = Depends(get_return_shelf_use_case),
):
    logical_task_ids = payload.logical_task_ids
    use_case.execute_return(logical_task_ids)
    return {"status": "RETURN_TRIGGERED"}
