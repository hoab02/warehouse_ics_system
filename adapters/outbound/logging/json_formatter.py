import json
import logging
from datetime import datetime, timezone

class JsonLogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": record.getMessage(),
            "logger": record.name,
        }

        # Business context (bắt buộc)
        context = getattr(record, "context", None)
        if context:
            log.update({
                "trace_id": context.trace_id,
                "scenario_id": context.scenario_id,
                "task_id": context.task_id,
                "source": context.source,
            })

        # Extra business fields
        fields = getattr(record, "fields", None)
        if fields:
            log.update(fields)

        # Exception (nếu có)
        if record.exc_info:
            log["exception"] = self.formatException(record.exc_info)

        return json.dumps(log, ensure_ascii=False)