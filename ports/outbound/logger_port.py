"""
    info    → business flow bình thường
    warning → bất thường nhưng chịu được
    error   → thất bại nghiệp vụ / kỹ thuật
"""

from typing import Protocol, Any, Mapping, Optional
from common.log_context import LogContext


class LoggerPort(Protocol):

    def info(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None
    ) -> None:
        ...

    def warning(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None
    ) -> None:
        ...

    def error(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> None:
        ...