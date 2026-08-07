from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

import pytest

from dtmo.connectors.provenance import IngestionContext, canonical_payload_digest, normalize_connector_records
from tools.validate_payload_provenance import build_evidence


RUN_ID = UUID("11111111-1111-4111-8111-111111111111")
FETCHED_AT = datetime(2026, 8, 7, 5, 40, tzinfo=UTC)


def context() -> IngestionContext:
    return IngestionContext(
        connector_id="cisa-kev-canary",
        run_id=RUN_ID,
        source_uri="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        fetched_at=FETCHED_AT,
        confidence=95,
    )


def test_candidate_retains_immutable_provenance_and_never_approves_publication() -> None:
    raw = {"cveID": "CVE-2026-1234", "dateAdded": "2026-08-06", "vulnerabilityName": "Example"}

    result = normalize_connector_records(
        [raw],
        context=context(),
        external_id_field="cveID",
        source_timestamp_field="dateAdded",
    )

    assert result.publish_approved is False
    assert result.quarantined == ()
    candidate = result.candidates[0]
    assert candidate.connector_id == "cisa-kev-canary"
    assert candidate.run_id == RUN_ID
    assert candidate.external_id == "CVE-2026-1234"
    assert candidate.source_uri.startswith("https://www.cisa.gov/")
    assert candidate.source_timestamp == "2026-08-06"
    assert candidate.fetched_at == FETCHED_AT
    assert candidate.payload_digest == canonical_payload_digest(raw)
    assert candidate.confidence == 95
    assert candidate.raw_evidence == raw
    assert candidate.publish_approved is False

    with pytest.raises(AttributeError):
        candidate.confidence = 1  # type: ignore[misc]


def test_payload_digest_is_deterministic_across_key_order() -> None:
    first = {"b": 2, "a": 1}
    second = {"a": 1, "b": 2}

    assert canonical_payload_digest(first) == canonical_payload_digest(second)


def test_malformed_and_duplicate_records_fail_closed_to_quarantine() -> None:
    first = {"cveID": "CVE-2026-1234", "dateAdded": "2026-08-06"}
    duplicate = {"dateAdded": "2026-08-07", "cveID": "CVE-2026-1234"}

    result = normalize_connector_records(
        [first, duplicate, "not-an-object", {"dateAdded": "2026-08-06"}],
        context=context(),
        external_id_field="cveID",
        source_timestamp_field="dateAdded",
    )

    assert len(result.candidates) == 1
    assert result.duplicate_count == 1
    assert {item.reason for item in result.quarantined} == {
        "duplicate_external_id",
        "malformed_record",
        "missing_external_id",
    }
    assert all(item.publish_approved is False for item in result.quarantined)
    assert all(len(item.payload_digest) == 64 for item in result.quarantined)


def test_malformed_source_timestamp_is_quarantined() -> None:
    result = normalize_connector_records(
        [{"cveID": "CVE-2026-9999", "dateAdded": 20260807}],
        context=context(),
        external_id_field="cveID",
        source_timestamp_field="dateAdded",
    )

    assert result.candidates == ()
    assert result.quarantined[0].reason == "malformed_source_timestamp"
    assert result.quarantined[0].publish_approved is False


def test_invalid_ingestion_context_fails_before_accepting_records() -> None:
    invalid = IngestionContext(
        connector_id="cisa-kev-canary",
        run_id=RUN_ID,
        source_uri="http://example.test/feed",
        fetched_at=FETCHED_AT,
        confidence=101,
    )

    with pytest.raises(ValueError):
        normalize_connector_records([{"id": "1"}], context=invalid, external_id_field="id")


def test_retained_evidence_never_reports_quarantine_as_publication_approved() -> None:
    evidence = build_evidence()

    assert evidence["publish_approved"] is False
    assert evidence["candidate_publish_approved"] is False
    assert evidence["quarantine_publish_approved"] is False
