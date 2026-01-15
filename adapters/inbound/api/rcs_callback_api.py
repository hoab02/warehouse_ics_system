from fastapi import APIRouter, HTTPException
from application.callback.rcs_callback_handler import RcsCallbackHandler

router = APIRouter()

@router.post("/callback")
def rcs_callback(payload: dict):
    try:
        mission_id = payload["mission_id"]
        status = payload["status"]
        RcsCallbackHandler.instance().handle(mission_id, status)
        return {"ok": True}
    except KeyError:
        raise HTTPException(400, "Invalid payload")


