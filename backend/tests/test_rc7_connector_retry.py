from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from dtmo.connectors.retry import (
    ConnectorRetryExhaustedError,
    ConnectorRetryPolicy,
    evaluate_connector_retry,
    require_connector_retry,
)


def test_exponential_backoff_is_bounded_and_deterministic() -> None:
    policy = ConnectorRetryPolicy(max_attempts=5, base_delay_seconds=2, max_delay_seconds=5)
    now = datetime(2026, 8, 7, 15, 0, tzinfo=UTC)

    first = evaluate_connector_retry("cisa-kev", failed_attempt=1, policy=policy, now=now)
    third = evaluate_connector_retry("cisa-kev", failed_attempt=3, policy=policy, now=now)

    assert first.retry_allowed is True
    assert first.reason == "exponential_backoff"
    assert first.delay_seconds == 2
    assert first.retry_at == now + timedelta(seconds=2)
    assert third.delay_seconds == 5
    assert third.retry_at == now + timedelta(seconds=5)
    assert first.publish_approved is False
    assert third.publish_approved is False


def test_provider_retry_after_is_honored_but_capped() -> None:
    policy = ConnectorRetryPolicy(max_attempts=4, max_retry_after_seconds=120)
    now = datetime(2026, 8, 7, 15, 0, tzinfo=UTC)

    within_cap = evaluate_connector_retry(
        "nvd", failed_attempt=1, policy=policy, retry_after_seconds=30, now=now
    )
    capped = evaluate_connector_retry(
        "nvd", failed_attempt=2, policy=policy, retry_after_seconds=900, now=now
    )

    assert within_cap.reason == "provider_retry_after"
    assert within_cap.delay_seconds == 30
    assert capped.delay_seconds == 120
    assert capped.retry_at == now + timedelta(seconds=120)
    assert within_cap.publish_approved is False
    assert capped.publish_approved is False


def test_invalid_provider_retry_after_fails_closed() -> None:
    decision = evaluate_connector_retry("cisa-kev", failed_attempt=1, retry_after_seconds=-1)

    assert decision.retry_allowed is False
    assert decision.reason == "invalid_retry_after"
    assert decision.retry_at is None
    assert decision.publish_approved is False


def test_attempt_exhaustion_fails_closed() -> None:
    policy = ConnectorRetryPolicy(max_attempts=3)
    decision = evaluate_connector_retry("cisa-kev", failed_attempt=3, policy=policy)

    assert decision.retry_allowed is False
    assert decision.reason == "attempts_exhausted"
    assert decision.delay_seconds is None
    assert decision.retry_at is None
    assert decision.publish_approved is False

    with pytest.raises(ConnectorRetryExhaustedError) as exc_info:
        require_connector_retry("cisa-kev", failed_attempt=3, policy=policy)
    assert exc_info.value.decision.publish_approved is False


def test_non_retryable_failure_fails_closed_before_budget_is_spent() -> None:
    decision = evaluate_connector_retry("cisa-kev", failed_attempt=1, retryable=False)

    assert decision.retry_allowed is False
    assert decision.reason == "non_retryable_failure"
    assert decision.publish_approved is False


def test_retry_state_is_connector_local() -> None:
    policy = ConnectorRetryPolicy(max_attempts=2)
    cisa = evaluate_connector_retry("cisa-kev", failed_attempt=2, policy=policy)
    nvd = evaluate_connector_retry("nvd", failed_attempt=1, policy=policy)

    assert cisa.retry_allowed is False
    assert cisa.reason == "attempts_exhausted"
    assert nvd.retry_allowed is True
    assert nvd.connector_id == "nvd"
    assert nvd.publish_approved is False


def test_invalid_policy_and_attempt_inputs_are_rejected() -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        ConnectorRetryPolicy(max_attempts=0)
    with pytest.raises(ValueError, match="connector_id"):
        evaluate_connector_retry("   ", failed_attempt=1)
    with pytest.raises(ValueError, match="failed_attempt"):
        evaluate_connector_retry("cisa-kev", failed_attempt=0)
