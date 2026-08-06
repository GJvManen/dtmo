from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from dtmo.connectors.canary import CanaryPolicy, parse_cisa_kev, run_live_canary


@pytest.fixture
def policy() -> CanaryPolicy:
    return CanaryPolicy(
        connector_id="cisa-kev-canary",
        source_url="https://example.test/kev.json",
        licence="public-domain",
        terms_url="https://example.test/terms",
        timeout_seconds=1.0,
        max_attempts=3,
        minimum_interval_seconds=0.1,
        maximum_records=10,
    )


@pytest.mark.asyncio
async def test_canary_preserves_provenance_quarantines_duplicates_and_never_publishes(
    policy: CanaryPolicy,
) -> None:
    payload: dict[str, Any] = {
        "vulnerabilities": [
            {"cveID": "CVE-2026-0001", "vulnerabilityName": "Example one", "dateAdded": "2026-08-06"},
            {"cveID": "CVE-2026-0001", "vulnerabilityName": "Duplicate", "dateAdded": "2026-08-06"},
            {"cveID": "", "vulnerabilityName": "Malformed", "dateAdded": "2026-08-06"},
        ]
    }

    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["user-agent"] == "DTMO-connector-canary/1.0"
        return httpx.Response(200, content=json.dumps(payload), request=request)

    evidence = await run_live_canary(policy, parse_cisa_kev, transport=httpx.MockTransport(handler))

    assert evidence.status == "completed"
    assert evidence.attempts == 1
    assert evidence.publish_approved is False
    assert evidence.duplicate_count == 1
    assert len(evidence.records) == 1
    assert len(evidence.quarantined) == 2
    record = evidence.records[0]
    assert record.source_url == policy.source_url
    assert record.source_reliability == "authoritative"
    assert record.confidence == 95
    assert len(record.evidence_hash) == 64


@pytest.mark.asyncio
async def test_canary_retries_with_bounded_backoff_and_fails_closed(policy: CanaryPolicy) -> None:
    calls = 0
    delays: list[float] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        return httpx.Response(503, request=request)

    async def fake_sleep(delay: float) -> None:
        delays.append(delay)

    evidence = await run_live_canary(
        policy,
        parse_cisa_kev,
        transport=httpx.MockTransport(handler),
        sleep=fake_sleep,
    )

    assert calls == 3
    assert delays == [0.1, 0.2]
    assert evidence.status == "failed"
    assert evidence.attempts == 3
    assert evidence.records == []
    assert evidence.publish_approved is False
    assert evidence.error


def test_canary_policy_requires_https_licence_and_bounded_attempts() -> None:
    with pytest.raises(ValueError, match="HTTPS"):
        CanaryPolicy("x", "http://example.test", "public", "https://example.test/terms")
    with pytest.raises(ValueError, match="licence"):
        CanaryPolicy("x", "https://example.test", "", "https://example.test/terms")
    with pytest.raises(ValueError, match="between 1 and 5"):
        CanaryPolicy("x", "https://example.test", "public", "https://example.test/terms", max_attempts=6)


def test_parser_quarantines_non_object_payload_items(policy: CanaryPolicy) -> None:
    records, quarantined, duplicates = parse_cisa_kev({"vulnerabilities": ["bad"]}, policy)
    assert records == []
    assert duplicates == 0
    assert quarantined[0].reason == "malformed_record"
