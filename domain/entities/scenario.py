from domain.fsm.scenario_fsm import ScenarioStatus


class Scenario:
    def __init__(self, scenario_id: str, scenario_type: str, stations: list, tasks: list):
        self.scenario_id = scenario_id
        self.tasks = sorted(tasks, key=lambda t: t.sequence)
        self.stations = stations
        self.scenario_type = scenario_type
        self.status = ScenarioStatus.CREATED

