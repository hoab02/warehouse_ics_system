import os
from logging.handlers import TimedRotatingFileHandler

class TimeSizeRotatingFileHandler(TimedRotatingFileHandler):

    def __init__(
        self,
        filename: str,
        when: str = "midnight",
        interval: int = 1,
        backupCount: int = 14,
        maxBytes: int = 100 * 1024 * 1024,  # 100MB
        encoding: str = "utf-8",
        utc: bool = True,
    ):
        self.maxBytes = maxBytes
        super().__init__(
            filename=filename,
            when=when,
            interval=interval,
            backupCount=backupCount,
            encoding=encoding,
            utc=utc,
        )

    def shouldRollover(self, record):
        # 1️⃣ Time-based rollover
        if super().shouldRollover(record):
            return True

        # 2️⃣ Size-based rollover
        if self.maxBytes > 0 and os.path.exists(self.baseFilename):
            if os.path.getsize(self.baseFilename) >= self.maxBytes:
                return True

        return False