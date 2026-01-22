from collections import defaultdict
from domain.exceptions import InvalidTaskOrderError, ScenarioValidationException

def validate_scenario_tasks(tasks):
    """
    Assumptions:
    - tasks đã được sort theo sequence (best effort)
    - cho phép nhiều task cùng shelf & station & side
    - side KHÔNG được đan xen trong cùng shelf & station
    """

    if not tasks:
        raise ScenarioValidationException("Scenario must contain at least one task")

    grouped = defaultdict(list)
    for task in tasks:
        grouped[(task.shelf_id, task.station_id)].append(task)

    for (shelf_id, station_id), group in grouped.items():

        sides_in_order = [task.side for task in group]

        seen_side_switch = False
        current_side = sides_in_order[0]

        for side in sides_in_order[1:]:
            if side != current_side:
                if seen_side_switch:
                    raise InvalidTaskOrderError(
                        f"SIDE_INTERLEAVING for shelf={shelf_id}, station={station_id}"
                    )
                seen_side_switch = True
                current_side = side

        sequences = [task.sequence for task in group]
        if sequences != sorted(sequences):
            raise InvalidTaskOrderError(
                f"SEQUENCE_NOT_ORDERED for shelf={shelf_id}, station={station_id}"
            )