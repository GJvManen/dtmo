from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest

from dtmo.connectors.timeout import (
    ConnectorTimedOutError,
    ConnectorTimeoutPolicy,
    run_connector_with_timeout,
)


@pytest.mark.asyncio
async def test_fast_operation_completes_without_publish_approval() -> None:
    async def operation() -> str:
        await asyncio.sleep(0)
        return "ok"

    observed = datetime(2026, 8, 7, 17, 0, tzinfo=UTC)
    value, decision = await run_connector_with_timeout(
        "cisa-kev",
        run_id="run-fast",
        source_uri="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        operation=operation(),
        policy=ConnectorTimeoutPolicy(timeout_seconds=0.2),
        observed_at=observed,
    )

    assert value == "ok"
    assert decision.allowed_to_continue is True
    assert decision.reason == "completed_within_timeout"
    assert decision.connector_id == "cisa-kev"
    assert decision.run_id == "run-fast"
    assert decision.observed_at == observed
    assert decision.publish_approved is False


@pytest.mark.asyncio
async def test_slow_operation_fails_closed_and_is_cancelled() -> None:
    cancelled = asyncio.Event()

    async def operation() -> None:
        try:
            await asyncio.sleep(60)
        finally:
            cancelled.set()

    with pytest.raises(ConnectorTimedOutError) as exc_info:
        await run_connector_with_timeout(
            "cisa-kev",
            run_id="run-timeout",
            source_uri="https://example.invalid/source",
            operation=operation(),
            policy=ConnectorTimeoutPolicy(timeout_seconds=0.01),
        )

    decision = exc_info.value.decision
    assert cancelled.is_set()
    assert decision.allowed_to_continue is False
    assert decision.reason == "timeout_budget_exhausted"
    assert decision.publish_approved is False


@pytest.mark.asyncio
async def test_timeout_is_connector_local_and_does_not_cancel_independent_source() -> None:
    slow_cancelled = asyncio.Event()

    async def slow() -> str:
        try:
            await asyncio.sleep(60)
            return "slow"
        finally:
            slow_cancelled.set()

    async def fast() -> str:
        await asyncio.sleep(0.001)
        return "nvd-ok"

    slow_task = asyncio.create_task(
        run_connector_with_timeout(
            "cisa-kev",
            run_id="run-cisa",
            source_uri="https://example.invalid/cisa",
            operation=slow(),
            policy=ConnectorTimeoutPolicy(timeout_seconds=0.01),
        )
    )
    fast_task = asyncio.create_task(
        run_connector_with_timeout(
            "nvd",
            run_id="run-nvd",
            source_uri="https://services.nvd.nist.gov/rest/json/cves/2.0",
            operation=fast(),
            policy=ConnectorTimeoutPolicy(timeout_seconds=0.2),
        )
    )

    fast_value, fast_decision = await fast_task
    assert fast_value == "nvd-ok"
    assert fast_decision.allowed_to_continue is True
    assert fast_decision.publish_approved is False

    with pytest.raises(ConnectorTimedOutError):
        await slow_task
    assert slow_cancelled.is_set()


@pytest.mark.asyncio
async def test_scheduler_cancellation_is_re_raised_not_converted_to_success() -> None:
    started = asyncio.Event()

    async def operation() -> None:
        started.set()
        await asyncio.sleep(60)

    guarded = asyncio.create_task(
        run_connector_with_timeout(
            "nvd",
            run_id="run-cancel",
            source_uri="https://services.nvd.nist.gov/rest/json/cves/2.0",
            operation=operation(),
            policy=ConnectorTimeoutPolicy(timeout_seconds=30),
        )
    )
    await started.wait()
    guarded.cancel()

    with pytest.raises(asyncio.CancelledError):
        await guarded


def test_policy_and_provenance_inputs_fail_closed() -> None:
    with pytest.raises(ValueError, match="timeout_seconds"):
        ConnectorTimeoutPolicy(timeout_seconds=0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("connector_id", "run_id", "source_uri", "field"),
    [
        ("", "run", "https://example.test", "connector_id"),
        ("cisa-kev", "", "https://example.test", "run_id"),
        ("cisa-kev", "run", "", "source_uri"),
    ],
)
async def test_missing_provenance_is_rejected(
    connector_id: str, run_id: str, source_uri: str, field: str
) -> None:
    async def operation() -> None:
        return None

    coroutine = operation()
    try:
        with pytest.raises(ValueError, match=field):
            await run_connector_with_timeout(
                connector_id,
                run_id=run_id,
                source_uri=source_uri,
                operation=coroutine,
            )
    finally:
        coroutine.close()
