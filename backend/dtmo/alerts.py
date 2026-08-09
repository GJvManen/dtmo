from __future__ import annotations

import re
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
QUEUE_BACKLOG_DEPTH = Gauge(
    "dtmo_queue_backlog_depth",
    "Observed queue backlog depth",
    ["queue"],
)
QUEUE_BACKLOG_CAPACITY = Gauge(
    "dtmo_queue_backlog_capacity",
    "Configured queue backlog capacity",
    ["queue"],
)
QUEUE_BACKLOG_UTILIZATION = Gauge(
    "dtmo_queue_backlog_utilization_ratio",
    "Observed queue backlog depth divided by capacity",
    ["queue"],
)
QUEUE_BACKLOG_ALERT_ACTIVE = Gauge(
    "dtmo_queue_backlog_alert_active",
    "Whether the queue backlog alert is active",
    ["queue"],
)
QUEUE_BACKLOG_ALERT_TRANSITIONS = Counter(
    "dtmo_queue_backlog_alert_transitions_total",
    "Queue backlog alert state transitions",
    ["queue", "transition"],
)
STORAGE_INTEGRITY_CHECKS = Counter(
    "dtmo_storage_integrity_checks_total",
    "Observed storage integrity check results",
    ["storage", "result"],
)
STORAGE_INTEGRITY_ALERT_ACTIVE = Gauge(
    "dtmo_storage_integrity_alert_active",
    "Whether a storage integrity failure alert is active",
    ["storage"],
)
STORAGE_INTEGRITY_ALERT_TRANSITIONS = Counter(
    "dtmo_storage_integrity_alert_transitions_total",
    "Storage integrity alert state transitions",
    ["storage", "transition"],
)

_CONNECTOR_ACTION = "Inspect connector health, upstream availability, credentials and rate limits."
_QUEUE_ACTION = (
    "Inspect consumers and downstream dependency health; drain backlog before increasing "
    "producer throughput."
)
_STORAGE_ACTION = (
    "Stop trusting the affected storage evidence, verify size and checksum receipts, and restore "
    "from known-good immutable evidence before reprocessing."
)
_QUEUE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$")
_STORAGE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,63}$")


def _current_correlation(value: str | None) -> str:
    current = value or correlation_id.get()
    return resolve_correlation_id(None) if current == "-" else current


@dataclass(frozen=True, slots=True)
class ConnectorAlertSignal:
    connector_id: str
    state: str
    transitioned: bool
    correlation_id: str
    action: str
    publish_approved: bool = False


@dataclass(frozen=True, slots=True)
class QueueBacklogAlertSignal:
    queue_name: str
    state: str
    transitioned: bool
    correlation_id: str
    depth: int
    capacity: int
    utilization_ratio: float
    action: str
    publish_approved: bool = False


@dataclass(frozen=True, slots=True)
class StorageIntegrityAlertSignal:
    storage_name: str
    state: str
    transitioned: bool
    correlation_id: str
    integrity_ok: bool
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

        current_correlation = _current_correlation(correlation)
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
                        action=_CONNECTOR_ACTION,
                        publish_approved=False,
                    )
                else:
                    self.log.warning(
                        "connector_alert_active",
                        connector_id=connector_id,
                        correlation_id=current_correlation,
                        severity="warning",
                        attempts=result.attempts,
                        action=_CONNECTOR_ACTION,
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
            action=(
                _CONNECTOR_ACTION
                if state == "active"
                else "Continue normal source-health monitoring."
            ),
            publish_approved=False,
        )


class QueueBacklogAlertManager:
    """Observe bounded queue utilization and emit hysteretic backlog alert evidence.

    The queue implementation remains authoritative for backpressure and recovery. This
    observer consumes only queue depth/capacity measurements. It raises at the configured
    utilization threshold and clears only at or below the lower recovery threshold, which
    prevents alert flapping near the raise boundary. It does not move queue items, change
    producer/consumer behavior, deliver notifications or grant publication approval.
    """

    def __init__(self, *, raise_ratio: float = 0.80, clear_ratio: float = 0.50) -> None:
        if not 0 <= clear_ratio < raise_ratio <= 1:
            raise ValueError("queue backlog thresholds must satisfy 0 <= clear < raise <= 1")
        self.raise_ratio = raise_ratio
        self.clear_ratio = clear_ratio
        self._active: set[str] = set()
        self._lock = Lock()
        self.log = get_logger("queue.alerts")

    def observe(
        self,
        queue_name: str,
        *,
        depth: int,
        capacity: int,
        correlation: str | None = None,
    ) -> QueueBacklogAlertSignal:
        name = queue_name.strip()
        if not _QUEUE_NAME.fullmatch(name):
            raise ValueError("queue_name must be a bounded operational queue identifier")
        if capacity <= 0:
            raise ValueError("queue capacity must be positive")
        if depth < 0 or depth > capacity:
            raise ValueError("queue depth must be between zero and capacity")

        current_correlation = _current_correlation(correlation)
        utilization = depth / capacity
        QUEUE_BACKLOG_DEPTH.labels(name).set(depth)
        QUEUE_BACKLOG_CAPACITY.labels(name).set(capacity)
        QUEUE_BACKLOG_UTILIZATION.labels(name).set(utilization)

        with self._lock:
            was_active = name in self._active
            if was_active and utilization <= self.clear_ratio:
                self._active.remove(name)
                state = "clear"
                transitioned = True
                QUEUE_BACKLOG_ALERT_ACTIVE.labels(name).set(0)
                QUEUE_BACKLOG_ALERT_TRANSITIONS.labels(name, "cleared").inc()
                self.log.info(
                    "queue_backlog_alert_cleared",
                    queue_name=name,
                    correlation_id=current_correlation,
                    severity="info",
                    depth=depth,
                    capacity=capacity,
                    utilization_ratio=round(utilization, 4),
                    raise_threshold=self.raise_ratio,
                    clear_threshold=self.clear_ratio,
                    action="Continue normal queue monitoring.",
                    publish_approved=False,
                )
            elif was_active:
                state = "active"
                transitioned = False
                QUEUE_BACKLOG_ALERT_ACTIVE.labels(name).set(1)
                self.log.warning(
                    "queue_backlog_alert_active",
                    queue_name=name,
                    correlation_id=current_correlation,
                    severity="warning",
                    depth=depth,
                    capacity=capacity,
                    utilization_ratio=round(utilization, 4),
                    raise_threshold=self.raise_ratio,
                    clear_threshold=self.clear_ratio,
                    action=_QUEUE_ACTION,
                    publish_approved=False,
                )
            elif utilization >= self.raise_ratio:
                self._active.add(name)
                state = "active"
                transitioned = True
                QUEUE_BACKLOG_ALERT_ACTIVE.labels(name).set(1)
                QUEUE_BACKLOG_ALERT_TRANSITIONS.labels(name, "raised").inc()
                self.log.warning(
                    "queue_backlog_alert_raised",
                    queue_name=name,
                    correlation_id=current_correlation,
                    severity="warning",
                    depth=depth,
                    capacity=capacity,
                    utilization_ratio=round(utilization, 4),
                    raise_threshold=self.raise_ratio,
                    clear_threshold=self.clear_ratio,
                    action=_QUEUE_ACTION,
                    publish_approved=False,
                )
            else:
                state = "clear"
                transitioned = False
                QUEUE_BACKLOG_ALERT_ACTIVE.labels(name).set(0)

        return QueueBacklogAlertSignal(
            queue_name=name,
            state=state,
            transitioned=transitioned,
            correlation_id=current_correlation,
            depth=depth,
            capacity=capacity,
            utilization_ratio=utilization,
            action=_QUEUE_ACTION if state == "active" else "Continue normal queue monitoring.",
            publish_approved=False,
        )


class StorageIntegrityAlertManager:
    """Observe trusted storage-verification outcomes without exposing stored evidence.

    Existing storage services remain authoritative for checksum/size verification and
    recovery. This observer consumes only a bounded storage name plus the boolean result.
    It never receives object keys, hashes or payload bytes, preventing those values from
    entering alert labels or logs. A failed verification raises/retains the alert and a
    later successful verification clears it. It does not mutate storage or approve sharing.
    """

    def __init__(self) -> None:
        self._active: set[str] = set()
        self._lock = Lock()
        self.log = get_logger("storage.alerts")

    def observe(
        self,
        storage_name: str,
        *,
        integrity_ok: bool,
        correlation: str | None = None,
    ) -> StorageIntegrityAlertSignal:
        name = storage_name.strip()
        if not _STORAGE_NAME.fullmatch(name):
            raise ValueError("storage_name must be a bounded operational storage identifier")

        current_correlation = _current_correlation(correlation)
        result = "pass" if integrity_ok else "fail"
        STORAGE_INTEGRITY_CHECKS.labels(name, result).inc()

        with self._lock:
            was_active = name in self._active
            if not integrity_ok:
                self._active.add(name)
                state = "active"
                transitioned = not was_active
                STORAGE_INTEGRITY_ALERT_ACTIVE.labels(name).set(1)
                if transitioned:
                    STORAGE_INTEGRITY_ALERT_TRANSITIONS.labels(name, "raised").inc()
                    event = "storage_integrity_alert_raised"
                else:
                    event = "storage_integrity_alert_active"
                self.log.warning(
                    event,
                    storage_name=name,
                    correlation_id=current_correlation,
                    severity="critical",
                    integrity_ok=False,
                    action=_STORAGE_ACTION,
                    publish_approved=False,
                )
            else:
                self._active.discard(name)
                state = "clear"
                transitioned = was_active
                STORAGE_INTEGRITY_ALERT_ACTIVE.labels(name).set(0)
                if transitioned:
                    STORAGE_INTEGRITY_ALERT_TRANSITIONS.labels(name, "cleared").inc()
                    self.log.info(
                        "storage_integrity_alert_cleared",
                        storage_name=name,
                        correlation_id=current_correlation,
                        severity="info",
                        integrity_ok=True,
                        action="Continue scheduled integrity verification.",
                        publish_approved=False,
                    )

        return StorageIntegrityAlertSignal(
            storage_name=name,
            state=state,
            transitioned=transitioned,
            correlation_id=current_correlation,
            integrity_ok=integrity_ok,
            action=_STORAGE_ACTION if state == "active" else "Continue scheduled integrity verification.",
            publish_approved=False,
        )


connector_alerts = ConnectorAlertManager()
queue_backlog_alerts = QueueBacklogAlertManager()
storage_integrity_alerts = StorageIntegrityAlertManager()
