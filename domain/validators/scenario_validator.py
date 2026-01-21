# app/domain/validators/scenario_validator.py
from collections import defaultdict
from domain.exceptions import DuplicateTaskError, InvalidSideMergeError, InvalidTaskOrderError
from domain.entities.task import Side

# def validate_scenario_tasks(tasks):
#     seen = set()
#
#     for task in tasks:
#         key = (task.shelf_id, task.station_id, task.side)
#         if key in seen:
#             raise DuplicateTaskError(
#                 f"Duplicate task: {key}"
#             )
#         seen.add(key)
#
#     # validate side merge adjacency
#     grouped = defaultdict(list)
#     for task in tasks:
#         grouped[(task.shelf_id, task.station_id)].append(task)
#
#     for (_, _), group in grouped.items():
#         if len(group) == 2:
#             sides = {t.side for t in group}
#             if sides == {Side.FRONT, Side.BACK}:
#                 seqs = sorted(t.sequence for t in group)
#                 if seqs[1] - seqs[0] != 1:
#                     raise InvalidSideMergeError(
#                         "LEFT and RIGHT tasks must be adjacent"
#                     )
#         elif len(group) > 2:
#             raise InvalidSideMergeError(
#                 "More than 2 tasks for same shelf & station"
#             )

def validate_scenario_tasks(tasks):
    """
    Assumptions:
    - tasks đã được sort theo sequence (best effort)
    - cho phép nhiều task cùng shelf & station & side
    - side KHÔNG được đan xen trong cùng shelf & station
    """

    # 1. Group theo shelf + station, nhưng GIỮ NGUYÊN THỨ TỰ
    grouped = defaultdict(list)
    for task in tasks:
        grouped[(task.shelf_id, task.station_id)].append(task)

    # 2. Validate từng group
    for (shelf_id, station_id), group in grouped.items():

        # 2.1 Validate side không đan xen
        sides_in_order = [task.side for task in group]

        seen_side_switch = False
        current_side = sides_in_order[0]

        for side in sides_in_order[1:]:
            if side != current_side:
                if seen_side_switch:
                    raise InvalidTaskOrderError(
                        f"Side interleaving detected for shelf={shelf_id}, station={station_id}"
                    )
                seen_side_switch = True
                current_side = side

        # 2.2 (Optional) validate sequence tăng dần
        sequences = [task.sequence for task in group]
        if sequences != sorted(sequences):
            raise InvalidTaskOrderError(
                f"Tasks not ordered by sequence for shelf={shelf_id}, station={station_id}"
            )