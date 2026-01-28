import uuid
from fastapi import Request
from infrastructure.logging.context import set_trace_id

async def logging_middleware(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id")
    if not trace_id:
        trace_id = str(uuid.uuid4())

    set_trace_id(trace_id)

    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response
