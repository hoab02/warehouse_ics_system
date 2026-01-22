from application.callback.rcs_callback_handler import RcsCallbackCommand
from adapters.inbound.api.mappers.rcs_status_mapper import RcsStatusMapper

def to_command(payload) -> RcsCallbackCommand:
    return RcsCallbackCommand(
        mission_id=payload.orderId.strip(),
        status=RcsStatusMapper.to_domain(
            payload.subTaskStatus,
            payload.status,
        )
    )
