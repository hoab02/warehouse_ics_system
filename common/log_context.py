from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class LogContext:
    trace_id: str
    scenario_id: Optional[str] = None
    task_id: Optional[str] = None
    source: Optional[str] = None  # API, RCS_CALLBACK, SCHEDULER