import logging
import os
from typing import Mapping, Any, Optional
from ports.outbound.logger_port import LoggerPort
from common.log_context import LogContext
from adapters.outbound.logging.json_formatter import JsonLogFormatter
from adapters.outbound.logging.rotating_time_size_handler import TimeSizeRotatingFileHandler


class FileLoggerAdapter(LoggerPort):

    def __init__(
        self,
        log_dir: str = "logs",
        log_file: str = "ics.log",
        level: int = logging.INFO,
        max_bytes: int = 100 * 1024 * 1024,
        retention_days: int = 14,
    ):
        os.makedirs(log_dir, exist_ok=True)

        self._logger = logging.getLogger("ICS")
        self._logger.setLevel(level)
        self._logger.propagate = False  # tránh log trùng root logger

        # Tránh add handler nhiều lần
        if not self._logger.handlers:
            handler = TimeSizeRotatingFileHandler(
                filename=os.path.join(log_dir, log_file),
                when="midnight",
                interval=1,
                backupCount=retention_days,
                maxBytes=max_bytes,
                utc=True,
            )
            handler.setFormatter(JsonLogFormatter())
            self._logger.addHandler(handler)

    def info(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None
    ) -> None:
        self._logger.info(
            event,
            extra={
                "context": context,
                "fields": fields,
            },
        )

    def warning(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None
    ) -> None:
        self._logger.warning(
            event,
            extra={
                "context": context,
                "fields": fields,
            },
        )

    def error(
        self,
        event: str,
        context: LogContext,
        fields: Optional[Mapping[str, Any]] = None,
        exception: Optional[Exception] = None
    ) -> None:
        self._logger.error(
            event,
            exc_info=exception,
            extra={
                "context": context,
                "fields": fields,
            },
        )