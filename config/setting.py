from pydantic import Field
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    """
    Application settings.
    Values are loaded from environment variables or .env file.
    """

    # =========================
    # APP
    # =========================
    app_name: str = "Mission Orchestrator"
    environment: str = Field(default="local")

    # =========================
    # MONGO
    # =========================
    mongo_uri: str = Field(
        default="mongodb://localhost:27017"
    )
    mongo_db: str = Field(
        default="mission_orchestrator"
    )

    # =========================
    # SCHEDULER
    # =========================
    scheduler_interval: int = Field(
        default=2,
        description="Scheduler tick interval in seconds"
    )

    # =========================
    # RCS
    # =========================
    rcs_base_url: str = Field(
        default="http://localhost:7000"
    ) # url addTask

    rcs_timeout: int = Field(
        default=5
    )

    # =========================
    # WSS
    # =========================
    wss_base_url: str = Field(
        default="http://localhost:8082"
    )
    wss_timeout: int = Field(
        default=5
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton-style settings instance
settings = Settings()
