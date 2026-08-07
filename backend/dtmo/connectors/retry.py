from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from dtmo.connectors.state import as_utc, utc_now


@dataclass(frozen=True, slots=True)
class ConnectorRetryPolicy:
    """Deterministic bounded retry policy for one connector execution.

    attempt is 1-based and represents the attempt that just failed. The policy returns
    whether another attempt may be scheduled and, if so, the earliest allowed time.
    Retry metadata is operational only and can never approve publication.
    """

    max_attempts: int = 4
    base_delay_seconds: float = 2.0
    max_delay_seconds: float = 60.0
    max_retry_after_seconds: float = 300.0

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.base_delay_seconds <= 0:
            raise ValueError("base_delay_seconds must be positive")
        if self.max_delay_seconds <= 0:
            raise ValueError("max_delay_seconds must be positive")
        if self.max_retry_after_seconds <= 0:
            raise ValueError("max_retry_after_seconds must be positive")


@dataclass(frozen=True, slots=True)
class ConnectorRetryDecision:
    connector_id: str
    failed_attempt: int
    retry_allowed: bool
    reason: str
    delay_seconds: float | None
    retry_at: datetime | None
    publish_approved: bool = False


class ConnectorRetryExhaustedError(RuntimeError):
    def __init__(self, decision: ConnectorRetryDecision) -> None:
        super().__init__(
            f"connector {decision.connector_id!r} retry blocked: {decision.reason} "
            f"after attempt {decision.failed_attempt}"
        )
        self.decision = decision


def evaluate_connector_retry(
    connector_id: str,
    *,
    failed_attempt: int,
    policy: ConnectorRetryPolicy | None = None,
    retryable: bool = True,
    retry_after_seconds: float | None = None,
    now: datetime | None = None,
) -> ConnectorRetryDecision:
    """Return a bounded, fail-closed retry decision for one connector.

    Provider Retry-After is honored when present, but bounded by
    ``max_retry_after_seconds``. Invalid or negative provider delay values fail closed.
    Without provider guidance, deterministic exponential backoff is used and capped by
    ``max_delay_seconds``. No jitter is applied here so CI evidence is reproducible.
    """

    normalized_id = connector_id.strip()
    if not normalized_id:
        raise ValueError("connector_id is required")
    if failed_attempt < 1:
        raise ValueError("failed_attempt must be positive")

    active_policy = policy or ConnectorRetryPolicy()
    current = as_utc(now or utc_now())

    if not retryable:
        return ConnectorRetryDecision(
            connector_id=normalized_id,
            failed_attempt=failed_attempt,
            retry_allowed=False,
            reason="non_retryable_failure",
            delay_seconds=None,
            retry_at=None,
            publish_approved=False,
        )

    if failed_attempt >= active_policy.max_attempts:
        return ConnectorRetryDecision(
            connector_id=normalized_id,
            failed_attempt=failed_attempt,
            retry_allowed=False,
            reason="attempts_exhausted",
            delay_seconds=None,
            retry_at=None,
            publish_approved=False,
        )

    if retry_after_seconds is not None:
        if retry_after_seconds < 0:
            return ConnectorRetryDecision(
                connector_id=normalized_id,
                failed_attempt=failed_attempt,
                retry_allowed=False,
                reason="invalid_retry_after",
                delay_seconds=None,
                retry_at=None,
                publish_approved=False,
            )
        delay = min(float(retry_after_seconds), active_policy.max_retry_after_seconds)
        reason = "provider_retry_after"
    else:
        delay = min(
            active_policy.base_delay_seconds * (2 ** (failed_attempt - 1)),
            active_policy.max_delay_seconds,
        )
        reason = "exponential_backoff"

    return ConnectorRetryDecision(
        connector_id=normalized_id,
        failed_attempt=failed_attempt,
        retry_allowed=True,
        reason=reason,
        delay_seconds=delay,
        retry_at=current + timedelta(seconds=delay),
        publish_approved=False,
    )


def require_connector_retry(*args: object, **kwargs: object) -> ConnectorRetryDecision:
    """Return an allowed retry or fail closed for exhausted/non-retryable failures."""

    decision = evaluate_connector_retry(*args, **kwargs)  # type: ignore[arg-type]
    if not decision.retry_allowed:
        raise ConnectorRetryExhaustedError(decision)
    return decision
