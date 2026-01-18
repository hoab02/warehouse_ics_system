import time
from threading import Thread
from fastapi import FastAPI


# =========================
# CONFIG
# =========================
from config.setting import settings

# =========================
# MONGO INFRASTRUCTURE
# =========================
from adapters.outbound.mongo.client import MongoClientProvider
from adapters.outbound.mongo.collections import ensure_indexes

from adapters.outbound.mongo.repositories.scenario_repo import (
    ScenarioMongoRepository
)
from adapters.outbound.mongo.repositories.execution_task_repo import (
    ExecutionTaskMongoRepository
)
from adapters.outbound.mongo.repositories.resource_lock_repository import (
    MongoResourceLockRepository
)


# =========================
# DOMAIN
# =========================


# =========================
# APPLICATION
# =========================
from application.use_cases.create_scenario import CreateScenarioUseCase
from application.scheduler.scheduler import Scheduler
from application.callback.rcs_callback_handler import RcsCallbackHandler
from application.service.mission_builder import MissionBuilder
from application.use_cases.return_shelf import ReturnShelfUseCase


# =========================
# OUTBOUND ADAPTERS
# =========================
from adapters.outbound.rcs.http_mission_adapter import RcsHttpMissionAdapter
from adapters.outbound.wss.http_notifier_adapter import WssHttpNotifierAdapter


# =========================
# INBOUND ADAPTERS (API)
# =========================
from adapters.inbound.api.scenario_api import router as scenario_router
from adapters.inbound.api.rcs_callback_api import router as rcs_callback_router
from adapters.inbound.api.return_shelf_api import router as return_shelf_router
# ======================================================
# 1️⃣ FASTAPI APP
# ======================================================
app = FastAPI(
    title="Mission Orchestrator",
    version="1.0.0"
)


# ======================================================
# 2️⃣ INIT MONGO
# ======================================================
mongo_provider = MongoClientProvider(
    uri=settings.mongo_uri,
    db_name=settings.mongo_db
)
db = mongo_provider.get_db()
ensure_indexes(db)


# ======================================================
# 3️⃣ REPOSITORIES (PORT IMPLEMENTATION)
# ======================================================
scenario_repository = ScenarioMongoRepository(db)
execution_task_repository = ExecutionTaskMongoRepository(db)
resource_lock_repository = MongoResourceLockRepository(db)


# ======================================================
# 4️⃣ DOMAIN SERVICES
# ======================================================


# ======================================================
# 5️⃣ OUTBOUND PORT ADAPTERS
# ======================================================
rcs_mission_port = RcsHttpMissionAdapter(
    base_url=settings.rcs_base_url
)

wss_notifier_port = WssHttpNotifierAdapter(
    base_url=settings.wss_base_url
)


# ======================================================
# 6️⃣ APPLICATION SERVICES
# ======================================================
mission_builder = MissionBuilder(
    callback_url=settings.rcs_callback_url
)

create_scenario_use_case = CreateScenarioUseCase(
    scenario_repo=scenario_repository,
    execution_task_repo=execution_task_repository
)

scheduler = Scheduler(
    scenario_repo=scenario_repository,
    execution_task_repo=execution_task_repository,
    resource_lock=resource_lock_repository,
    rcs_mission_port=rcs_mission_port,
    mission_builder=mission_builder
)

rcs_callback_handler = RcsCallbackHandler(
    execution_task_repo=execution_task_repository,
    scenario_repo=scenario_repository,
    resource_lock=resource_lock_repository,
    status_notifier=wss_notifier_port
)

return_shelf_use_cases = ReturnShelfUseCase(
    execution_task_repo=execution_task_repository,
    rcs_mission_port=rcs_mission_port,
    mission_builder=mission_builder
)

# ======================================================
# 7️⃣ API ROUTERS
# ======================================================
app.include_router(
    scenario_router,
    prefix="/api/v1/scenarios",
    tags=["Scenario"]
)

app.include_router(
    rcs_callback_router,
    prefix="/api/rcs/callback",
    tags=["RCS Callback"]
)

app.include_router(
    return_shelf_router,
    prefix="/api/v1",
    tags=["Return Shelf"]
)


# ======================================================
# 8️⃣ SCHEDULER LOOP
# ======================================================
def scheduler_loop():
    """
    Background loop for dispatching execution tasks.
    """
    while True:
        try:
            scheduler.tick()
        except Exception as exc:
            # LOG PROPERLY IN REAL SYSTEM
            print(f"[Scheduler error] {exc}")
        time.sleep(settings.scheduler_interval)


@app.on_event("startup")
def on_startup():
    """
    Start scheduler background thread
    """
    thread = Thread(target=scheduler_loop, daemon=True)
    thread.start()


