from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks

from adapters.inbound.api.mappers.rcs_callback_mapper import to_command
from application.callback.rcs_callback_handler import RcsCallbackHandler
from adapters.inbound.api.schemas import RcsCallbackPayload

router = APIRouter()

def get_rcs_callback_handler():
    from main import rcs_callback_handler
    return rcs_callback_handler

@router.post("")
def rcs_callback(
    payload: RcsCallbackPayload,
    background_tasks: BackgroundTasks,
    handler: RcsCallbackHandler = Depends(get_rcs_callback_handler),
):
    try:
        command = to_command(payload)
        background_tasks.add_task(handler.handle, command)
        return {"ok": True}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))