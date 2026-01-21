# app/domain/mergers/task_merger.py
from domain.entities.execution_task import ExecutionTask, CompletedPickingTask
from domain.entities.task import Side

# def merge_tasks(scenario_id, tasks):
#     execution_tasks = []
#     i = 0
#
#     while i < len(tasks):
#         current = tasks[i]
#
#         # check merge candidate
#         if (
#             i + 1 < len(tasks)
#             and current.shelf_id == tasks[i + 1].shelf_id
#             and current.station_id == tasks[i + 1].station_id
#             and current.side != tasks[i + 1].side
#         ):
#             next_task = tasks[i + 1]
#
#             actions = [
#                 "MOVE",
#                 f"ROTATE_{current.side}",
#                 f"ROTATE_{next_task.side}",
#             ]
#
#             execution_tasks.append(
#                 ExecutionTask(
#                     base_sequence=current.sequence,
#                     scenario_id = scenario_id,
#                     station_id=current.station_id,
#                     shelf_id=current.shelf_id,
#                     actions=actions,
#                     logical_task_ids=
#                     f"{scenario_id}:{current.sequence}&{next_task.sequence}"
#                 )
#             )
#             i += 2
#         else:
#             actions = [
#                 "MOVE",
#                 f"ROTATE_{current.side}",
#             ]
#             execution_tasks.append(
#                 ExecutionTask(
#                     base_sequence=current.sequence,
#                     scenario_id=scenario_id,
#                     station_id=current.station_id,
#                     shelf_id=current.shelf_id,
#                     actions=actions,
#                     logical_task_ids=f"{scenario_id}:{current.sequence}",
#                 )
#             )
#             i += 1
#
#     return execution_tasks


def merge_tasks(scenario_id, tasks):
    execution_tasks = []
    i = 0

    while i < len(tasks):
        first = tasks[i]

        block = [first]
        i += 1

        while i < len(tasks):
            t = tasks[i]
            if (
                t.shelf_id == first.shelf_id
                and t.station_id == first.station_id
            ):
                block.append(t)
                i += 1
            else:
                break


        front_tasks = [t for t in block if t.side == Side.FRONT]
        back_tasks = [t for t in block if t.side == Side.BACK]

        if front_tasks and back_tasks:
            need_rotate = True
            main_side = (
                Side.FRONT if len(front_tasks) >= len(back_tasks) else Side.BACK
            )
        else:
            need_rotate = False
            main_side = block[0].side


        completed_tasks = [
            CompletedPickingTask(
                picking_session_code=t.picking_session_code,
                picking_task_code=t.picking_task_code,
                or_code=t.or_code,
            )
            for t in block
        ]

        execution_tasks.append(
            ExecutionTask(
                scenario_id=scenario_id,
                shelf_id=first.shelf_id,
                station_id=first.station_id,
                logical_task_ids = f"{scenario_id}:merge{len(block)}",
                target_side=main_side,
                need_rotate=need_rotate,
                base_sequence=first.sequence,
                merged_picking_tasks=completed_tasks,
            )
        )

    return execution_tasks
