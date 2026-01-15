class Collections:
    SCENARIOS = "scenarios"
    EXECUTION_TASKS = "execution_tasks"
    STATION_LOCKS = "station_locks"
    SHELF_LOCKS = "shelf_locks"

def ensure_indexes(db):
    db[Collections.EXECUTION_TASKS].create_index("scenario_id")
    db[Collections.EXECUTION_TASKS].create_index("status")