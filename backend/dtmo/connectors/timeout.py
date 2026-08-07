from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, TypeVar

from dtmo.connectors.state import as_utc, utc_now

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ConnectorTimeoutPolicy:
    """Bound one connector invocation without granting publication authority."""

    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ConnectorTimeoutDecision:
    connector_id: str
    run_id: str
    source_uri: str
    allowed_to_continue: bool
    reason: str
    timeout_seconds: float
    observed_at: datetime
    publish_approved: bool = False


class ConnectorTimedOutError(RuntimeError):
    def __init__(self, decision: ConnectorTimeoutDecision) -> None:
        super().__init__(
            f"connector {decision.connector_id!r} run {decision.run_id!r} exceeded "
            f"{decision.timeout_seconds:g}s timeout budget"
        )
        self.decision = decision


def _normalize_required(value: str, field: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field} is required")
    return normalized


async def run_connector_with_timeout(
    connector_id: str,
    *,
    run_id: str,
    source_uri: str,
    operation: Awaitable[T],
    policy: ConnectorTimeoutPolicy | None = None,
    observed_at: datetime | None = None,
) -> tuple[T, ConnectorTimeoutDecision]:
    """Execute one connector operation inside a deterministic timeout budget.

    ``asyncio.wait_for`` cancels only the task created for this invocation when the
    budget expires. External cancellation is deliberately re-raised so scheduler or
    shutdown cancellation cannot be misclassified as a successful connector result.
    Provenance fields are mandatory on every decision and publication approval is
    always false: ingestion success is never equivalent to human share approval.
    """

    normalized_id = _normalize_required(connector_id, "connector_id")
    normalized_run_id = _normalize_required(run_id, "run_id")
    normalized_source_uri = _normalize_required(source_uri, "source_uri")
    active_policy = policy or ConnectorTimeoutPolicy()
    timestamp = as_utc(observed_at or utc_now())

    task = asyncio.ensure_future(operation)
    try:
        value = await asyncio.wait_for(task, timeout=active_policy.timeout_seconds)
    except TimeoutError as exc:
        decision = ConnectorTimeoutDecision(
            connector_id=normalized_id,
            run_id=normalized_run_id,
            source_uri=normalized_source_uri,
            allowed_to_continue=False,
            reason="timeout_budget_exhausted",
            timeout_seconds=active_policy.timeout_seconds,
            observed_at=timestamp,
            publish_approved=False,
        )
        raise ConnectorTimedOutError(decision) from exc
    except asyncio.CancelledError:
        if not task.done():
            task.cancel()
        raise

    decision = ConnectorTimeoutDecision(
        connector_id=normalized_id,
        run_id=normalized_run_id,
        source_uri=normalized_source_uri,
        allowed_to_continue=True,
        reason="completed_within_timeout",
        timeout_seconds=active_policy.timeout_seconds,
        observed_at=timestamp,
        publish_approved=False,
    )
    return value, decision
