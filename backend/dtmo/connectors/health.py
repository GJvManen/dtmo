from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from dtmo.connectors.state import ConnectorRuntimeState, ConnectorStateStore, as_utc, utc_now


@dataclass(frozen=True, slots=True)
class ConnectorExecutionDecision:
    """Fail-closed execution decision for one connector.

    Health state is scoped to a single connector identifier. The decision is operational
    metadata only and can never approve publication of intelligence.
    """

    connector_id: str
    allowed: bool
    reason: str
    health_status: str
    consecutive_failures: int
    retry_at: datetime | None
    publish_approved: bool = False


class ConnectorIsolatedError(RuntimeError):
    def __init__(self, decision: ConnectorExecutionDecision) -> None:
        super().__init__(
            f"connector {decision.connector_id!r} is isolated until "
            f"{decision.retry_at.isoformat() if decision.retry_at else 'health recovery'}"
        )
        self.decision = decision


def evaluate_connector_execution(
    store: ConnectorStateStore,
    connector_id: str,
    *,
    now: datetime | None = None,
) -> ConnectorExecutionDecision:
    """Evaluate whether one connector may execute without affecting other sources.

    A currently open circuit blocks execution. Once the isolation window expires, one
    caller may attempt recovery under the normal scheduler cadence; subsequent failure
    recording re-opens the circuit according to the store's configured threshold.
    """

    normalized_id = connector_id.strip()
    if not normalized_id:
        raise ValueError("connector_id is required")

    current = as_utc(now or utc_now())
    state = store.session.get(ConnectorRuntimeState, normalized_id)
    if state is None:
        return ConnectorExecutionDecision(
            connector_id=normalized_id,
            allowed=True,
            reason="no_health_history",
            health_status="unknown",
            consecutive_failures=0,
            retry_at=None,
            publish_approved=False,
        )

    retry_at = as_utc(state.circuit_open_until) if state.circuit_open_until else None
    if retry_at is not None and retry_at > current:
        return ConnectorExecutionDecision(
            connector_id=normalized_id,
            allowed=False,
            reason="circuit_open",
            health_status=state.health_status,
            consecutive_failures=state.consecutive_failures,
            retry_at=retry_at,
            publish_approved=False,
        )

    reason = "recovery_probe" if state.health_status == "isolated" else "health_allows_execution"
    return ConnectorExecutionDecision(
        connector_id=normalized_id,
        allowed=True,
        reason=reason,
        health_status=state.health_status,
        consecutive_failures=state.consecutive_failures,
        retry_at=retry_at,
        publish_approved=False,
    )


def require_connector_execution(
    store: ConnectorStateStore,
    connector_id: str,
    *,
    now: datetime | None = None,
) -> ConnectorExecutionDecision:
    """Return a permit or fail closed while the connector circuit is open."""

    decision = evaluate_connector_execution(store, connector_id, now=now)
    if not decision.allowed:
        raise ConnectorIsolatedError(decision)
    return decision
