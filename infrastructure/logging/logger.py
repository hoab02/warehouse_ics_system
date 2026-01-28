import logging
import os
from logging.handlers import TimedRotatingFileHandler
from infrastructure.logging.filter import TraceIdFilter


LOG_DIR = "logs"


def setup_logging():
    os.makedirs(LOG_DIR, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | trace=%(trace_id)s | %(message)s"
    )

    file_handler = TimedRotatingFileHandler(
        os.path.join(LOG_DIR, "app.log"),
        when="midnight",
        backupCount=14,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers.clear()

    file_handler.addFilter(TraceIdFilter())
    console_handler.addFilter(TraceIdFilter())

    root.addHandler(file_handler)
    root.addHandler(console_handler)

    # 👇 GẮN TRACE FILTER
    root.addFilter(TraceIdFilter())


