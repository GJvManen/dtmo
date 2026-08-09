from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from prometheus_client import Counter, Gauge

from dtmo.connectors.base import ConnectorResult
from dtmo.logging import correlation_id, get_logger, resolve_correlation_id

CONNECTOR_RUNS = Counter(
    "dtmo_connector_runs_total",
    "Terminal connector run results",
    ["connector", "status"],
)
CONNECTOR_ALERT_ACTIVE = Gauge(
    "dtmo_connector_alert_active",
    "Whether a terminal connector failure alert is active",
    ["connector"],
)
CONNECTOR_ALERT_TRANSITIONS = Counter(
    "dtmo_connector_alert_transitions_total",
    "Connector alert state transitions",
    ["connector", "transition"],
)

_ACTION = "Inspect connector health, upstream availability, credentials and rate limits."


@dataclass(frozen=True, slots=True)
class ConnectorAlertSignal:
    connector_id: str
    state: str
    transitioned: bool
    correlation_id: str
    action: str
    publish_approved: bool = False


class ConnectorAlertManager:
    """Emit bounded connector-failure signals without changing publication state.

    A connector's own retry policy remains authoritative for deciding when a run has
    terminally failed. This manager observes that terminal result, exposes a bounded
    Prometheus signal and emits structured transition events. A later successful run
    clears the alert. It does not deliver notifications or grant publication approval.
    """

    def __init__(self) -> None:
        self._active: set[str] = set()
        self._lock = Lock()
        self.log = get_logger("connector.alerts")

    def record(
        self,
        result: ConnectorResult,
        *,
        correlation: str | None = None,
    ) -> ConnectorAlertSignal:
        connector_id = result.connector_id.strip()
        if not connector_id:
            raise ValueError("connector_id is required")
        if result.status not in {"completed", "failed"}:
            raise ValueError("connector result status must be completed or failed")

        current_correlation = correlation or correlation_id.get()
        if current_correlation == "-":
            current_correlation = resolve_correlation_id(None)

        CONNECTOR_RUNS.labels(connector_id, result.status).inc()

        with self._lock:
            was_active = connector_id in self._active
            if result.status == "failed":
                self._active.add(connector_id)
                CONNECTOR_ALERT_ACTIVE.labels(connector_id).set(1)
                transitioned = not was_active
                state = "active"
                if transitioned:
                    CONNECTOR_ALERT_TRANSITIONS.labels(connector_id, "raised").inc()
                    self.log.warning(
                        "connector_alert_raised",
                        connector_id=connector_id,
                        correlation_id=current_correlation,
                        severity="warning",
                        attempts=result.attempts,
                        error_present=result.error is not None,
                        action=_ACTION,
                        publish_approved=False,
                    )
                else:
                    self.log.warning(
                        "connector_alert_active",
                        connector_id=connector_id,
                        correlation_id=current_correlation,
                        severity="warning",
                        attempts=result.attempts,
                        action=_ACTION,
                        publish_approved=False,
                    )
            else:
                self._active.discard(connector_id)
                CONNECTOR_ALERT_ACTIVE.labels(connector_id).set(0)
                transitioned = was_active
                state = "clear"
                if transitioned:
                    CONNECTOR_ALERT_TRANSITIONS.labels(connector_id, "cleared").inc()
                    self.log.info(
                        "connector_alert_cleared",
                        connector_id=connector_id,
                        correlation_id=current_correlation,
                        severity="info",
                        attempts=result.attempts,
                        action="No action required; continue normal source-health monitoring.",
                        publish_approved=False,
                    )

        return ConnectorAlertSignal(
            connector_id=connector_id,
            state=state,
            transitioned=transitioned,
            correlation_id=current_correlation,
            action=_ACTION if state == "active" else "Continue normal source-health monitoring.",
            publish_approved=False,
        )


connector_alerts = ConnectorAlertManager()
