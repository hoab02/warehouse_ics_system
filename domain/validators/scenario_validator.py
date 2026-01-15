# app/domain/validators/scenario_validator.py
from collections import defaultdict
from domain.exceptions import DuplicateTaskError, InvalidSideMergeError
from domain.entities.task import Side

def validate_scenario_tasks(tasks):
    seen = set()

    for task in tasks:
        key = (task.shelf_id, task.station_id, task.side)
        if key in seen:
            raise DuplicateTaskError(
                f"Duplicate task: {key}"
            )
        seen.add(key)

    # validate side merge adjacency
    grouped = defaultdict(list)
    for task in tasks:
        grouped[(task.shelf_id, task.station_id)].append(task)

    for (_, _), group in grouped.items():
        if len(group) == 2:
            sides = {t.side for t in group}
            if sides == {Side.FRONT, Side.BACK}:
                seqs = sorted(t.sequence for t in group)
                if seqs[1] - seqs[0] != 1:
                    raise InvalidSideMergeError(
                        "LEFT and RIGHT tasks must be adjacent"
                    )
        elif len(group) > 2:
            raise InvalidSideMergeError(
                "More than 2 tasks for same shelf & station"
            )
