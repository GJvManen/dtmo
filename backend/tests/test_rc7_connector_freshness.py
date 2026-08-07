from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from dtmo.connectors.provenance import IngestionContext, SourceFreshnessPolicy, normalize_connector_records


RUN_ID = UUID("77777777-7777-4777-8777-777777777777")
FETCHED_AT = datetime(2026, 8, 7, 11, 30, tzinfo=UTC)
POLICY = SourceFreshnessPolicy(max_age=timedelta(hours=24), max_future_skew=timedelta(minutes=5))


def context() -> IngestionContext:
    return IngestionContext(
        connector_id="cisa-kev-canary",
        run_id=RUN_ID,
        source_uri="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        fetched_at=FETCHED_AT,
        confidence=95,
    )


def normalize(records: list[dict[str, str]]):
    return normalize_connector_records(
        records,
        context=context(),
        external_id_field="cveID",
        source_timestamp_field="observedAt",
        freshness_policy=POLICY,
    )


def test_fresh_source_is_classified_and_provenance_is_preserved() -> None:
    result = normalize([{"cveID": "CVE-2026-1000", "observedAt": "2026-08-07T10:45:00Z"}])

    assert result.quarantined == ()
    candidate = result.candidates[0]
    assert candidate.source_timestamp == "2026-08-07T10:45:00Z"
    assert candidate.source_timestamp_utc == datetime(2026, 8, 7, 10, 45, tzinfo=UTC)
    assert candidate.freshness_status == "fresh"
    assert candidate.publish_approved is False
    assert result.publish_approved is False


def test_stale_source_fails_closed_to_quarantine() -> None:
    result = normalize([{"cveID": "CVE-2026-1001", "observedAt": "2026-08-06T10:00:00Z"}])

    assert result.candidates == ()
    item = result.quarantined[0]
    assert item.reason == "stale_source_timestamp"
    assert item.freshness_status == "stale"
    assert item.source_timestamp_utc == datetime(2026, 8, 6, 10, 0, tzinfo=UTC)
    assert item.publish_approved is False


def test_excessive_future_clock_skew_fails_closed() -> None:
    result = normalize([{"cveID": "CVE-2026-1002", "observedAt": "2026-08-07T11:36:00Z"}])

    assert result.candidates == ()
    item = result.quarantined[0]
    assert item.reason == "future_source_timestamp"
    assert item.freshness_status == "future_skew"
    assert item.publish_approved is False


def test_future_timestamp_within_skew_budget_is_fresh() -> None:
    result = normalize([{"cveID": "CVE-2026-1003", "observedAt": "2026-08-07T11:34:59+00:00"}])

    assert result.quarantined == ()
    assert result.candidates[0].freshness_status == "fresh"


def test_invalid_and_missing_timestamp_fail_closed() -> None:
    invalid = normalize([{"cveID": "CVE-2026-1004", "observedAt": "not-a-time"}])
    missing = normalize([{"cveID": "CVE-2026-1005"}])

    assert invalid.candidates == ()
    assert invalid.quarantined[0].reason == "malformed_source_timestamp"
    assert invalid.quarantined[0].freshness_status == "invalid"
    assert missing.candidates == ()
    assert missing.quarantined[0].reason == "missing_source_timestamp"
    assert missing.quarantined[0].freshness_status == "missing"
    assert all(item.publish_approved is False for item in (*invalid.quarantined, *missing.quarantined))


def test_missing_timestamp_may_only_be_allowed_by_explicit_policy() -> None:
    policy = SourceFreshnessPolicy(max_age=timedelta(hours=24), allow_missing=True)
    result = normalize_connector_records(
        [{"cveID": "CVE-2026-1006"}],
        context=context(),
        external_id_field="cveID",
        source_timestamp_field="observedAt",
        freshness_policy=policy,
    )

    assert result.quarantined == ()
    assert result.candidates[0].freshness_status == "missing_allowed"
    assert result.candidates[0].publish_approved is False


def test_invalid_freshness_policy_fails_before_ingestion() -> None:
    with pytest.raises(ValueError):
        normalize_connector_records(
            [{"cveID": "CVE-2026-1007", "observedAt": "2026-08-07T11:00:00Z"}],
            context=context(),
            external_id_field="cveID",
            source_timestamp_field="observedAt",
            freshness_policy=SourceFreshnessPolicy(max_age=timedelta(0)),
        )

    with pytest.raises(ValueError):
        normalize_connector_records(
            [{"cveID": "CVE-2026-1008"}],
            context=context(),
            external_id_field="cveID",
            freshness_policy=POLICY,
        )
