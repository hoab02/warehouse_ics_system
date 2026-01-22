class StatusNotifier:
    """
    Thin wrapper over WssNotifierPort
    """

    def __init__(self, wss_notifier_port):
        self.wss_notifier_port = wss_notifier_port

    def notify_execution_task(self, mission):
        self.wss_notifier_port.notify_execution_task(mission)

    def notify_scenario(self, scenario_id, status):
        self.wss_notifier_port.notify_scenario(scenario_id, status)