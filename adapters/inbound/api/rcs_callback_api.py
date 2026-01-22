from fastapi import APIRouter, HTTPException, Depends

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
    handler: RcsCallbackHandler = Depends(get_rcs_callback_handler),
):
    try:
        command = to_command(payload)
        handler.handle(command)
        return {"ok": True}
    except ValueError as e:
        # business error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        # unexpected error
        raise HTTPException(status_code=500, detail="Internal Error")
