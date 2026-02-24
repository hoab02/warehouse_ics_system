import requests

from ports.outbound.wss_notifier_port import WssNotifierPort
from ports.outbound.logger_port import LoggerPort
from common.log_context import LogContext


class WssHttpNotifierAdapter(WssNotifierPort):

    def __init__(
        self,
        base_url: str,
        timeout: int,
        logger: LoggerPort,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._logger = logger

    def notify_execution_task(self, mission: dict):
        context = LogContext(
            trace_id=mission.get("trace_id", "UNKNOWN"),
            scenario_id=mission.get("scenario_id"),
            task_id=None,
            source="WSS_NOTIFIER",
        )

        url = f"{self.base_url}/wos-orchestrator/api/v1/picking/robot-finish-picking-turn"

        self._logger.info(
            event="WSS_NOTIFY_EXECUTION_TASK_REQUEST",
            context=context,
            fields={"url": url, "payload": mission},
        )

        try:
            response = requests.post(url, json=mission, timeout=self.timeout)

            if response.status_code >= 400:
                self._logger.warning(
                    event="WSS_NOTIFY_EXECUTION_TASK_FAILED",
                    context=context,
                    fields={
                        "status_code": response.status_code,
                        "response": response.text,
                    },
                )
                response.raise_for_status()

            self._logger.info(
                event="WSS_NOTIFY_EXECUTION_TASK_SUCCESS",
                context=context,
                fields={"status_code": response.status_code},
            )

        except requests.RequestException as e:
            self._logger.error(
                event="WSS_NOTIFY_EXECUTION_TASK_ERROR",
                context=context,
                exception=e,
            )
            raise

    def notify_scenario(self, scenario_id: str, status: str):
        context = LogContext(
            trace_id=scenario_id,
            scenario_id=scenario_id,
            task_id=None,
            source="WSS_NOTIFIER",
        )

        url = f"{self.base_url}/wos-orchestrator/api/v1/picking/done-picking-task-turn"
        payload = {"scenario_id": scenario_id, "status": status}

        self._logger.info(
            event="WSS_NOTIFY_SCENARIO_REQUEST",
            context=context,
            fields={"url": url, "payload": payload},
        )

        try:
            response = requests.patch(url, json=payload, timeout=self.timeout)

            if response.status_code >= 400:
                self._logger.warning(
                    event="WSS_NOTIFY_SCENARIO_FAILED",
                    context=context,
                    fields={
                        "status_code": response.status_code,
                        "response": response.text,
                    },
                )
                response.raise_for_status()

            self._logger.info(
                event="WSS_NOTIFY_SCENARIO_SUCCESS",
                context=context,
                fields={"status_code": response.status_code},
            )

        except requests.RequestException as e:
            self._logger.error(
                event="WSS_NOTIFY_SCENARIO_ERROR",
                context=context,
                exception=e,
            )
            raise