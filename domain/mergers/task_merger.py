# app/domain/mergers/task_merger.py
from domain.entities.execution_task import ExecutionTask
from domain.entities.task import Side

def merge_tasks(scenario_id, tasks):
    execution_tasks = []
    i = 0

    while i < len(tasks):
        current = tasks[i]

        # check merge candidate
        if (
            i + 1 < len(tasks)
            and current.shelf_id == tasks[i + 1].shelf_id
            and current.station_id == tasks[i + 1].station_id
            and current.side != tasks[i + 1].side
        ):
            next_task = tasks[i + 1]

            actions = [
                "MOVE",
                f"ROTATE_{current.side}",
                f"ROTATE_{next_task.side}",
            ]

            execution_tasks.append(
                ExecutionTask(
                    scenario_id = scenario_id,
                    station_id=current.station_id,
                    shelf_id=current.shelf_id,
                    actions=actions,
                    logical_task_ids=
                    f"{scenario_id}:{current.sequence}&{next_task.sequence}"
                )
            )
            i += 2
        else:
            actions = [
                "MOVE",
                f"ROTATE_{current.side}",
            ]
            execution_tasks.append(
                ExecutionTask(
                    scenario_id=scenario_id,
                    station_id=current.station_id,
                    shelf_id=current.shelf_id,
                    actions=actions,
                    logical_task_ids=f"{scenario_id}:{current.sequence}",
                )
            )
            i += 1

    return execution_tasks
