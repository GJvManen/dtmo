from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from dtmo.audit.chain import AuditDecision, AuditEvent, append_audit_event
from dtmo.privacy import EvidenceDisposition, minimize_audit_event, retention_disposition

SECRET = b"p" * 32


def _event(*, occurred_at: datetime) -> AuditEvent:
    return append_audit_event(
        (),
        principal="analyst@example.test",
        principal_type="human",
        action="token.revoke",
        resource="token:jti:sensitive-token-id",
        decision=AuditDecision.ALLOW,
        request_id="request-sensitive-id",
        provenance_reference='{"reason":"credential theft"}',
        occurred_at=occurred_at,
        event_id=uuid4(),
    )


def test_minimized_projection_removes_direct_identity_and_token_identifiers() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    event = _event(occurred_at=now - timedelta(days=1))
    projection = minimize_audit_event(event, secret=SECRET, now=now, retention_days=90)

    serialized = repr(projection)
    assert "analyst@example.test" not in serialized
    assert "sensitive-token-id" not in serialized
    assert "request-sensitive-id" not in serialized
    assert projection.principal_reference.startswith("principal:v1:")
    assert projection.resource_reference.startswith("resource:v1:")
    assert projection.request_reference.startswith("request:v1:")
    assert projection.event_hash == event.event_hash
    assert projection.disposition is EvidenceDisposition.KEEP


def test_pseudonyms_are_stable_per_purpose_but_not_cross_linkable() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    event = _event(occurred_at=now - timedelta(days=1))
    first = minimize_audit_event(event, secret=SECRET, now=now, retention_days=90)
    second = minimize_audit_event(event, secret=SECRET, now=now, retention_days=90)
    assert first.principal_reference == second.principal_reference
    assert first.principal_reference != first.request_reference


def test_retention_expiry_and_legal_hold_override() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    occurred_at = now - timedelta(days=91)
    assert (
        retention_disposition(occurred_at=occurred_at, now=now, retention_days=90)
        is EvidenceDisposition.EXPIRE
    )
    assert (
        retention_disposition(
            occurred_at=occurred_at,
            now=now,
            retention_days=90,
            legal_hold=True,
        )
        is EvidenceDisposition.LEGAL_HOLD
    )


def test_retention_rejects_naive_timestamps_and_future_evidence() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    with pytest.raises(ValueError, match="timezone-aware"):
        retention_disposition(
            occurred_at=datetime(2026, 8, 1),
            now=now,
            retention_days=90,
        )
    with pytest.raises(ValueError, match="future"):
        retention_disposition(
            occurred_at=now + timedelta(seconds=1),
            now=now,
            retention_days=90,
        )


def test_minimization_requires_strong_secret() -> None:
    now = datetime(2026, 8, 6, tzinfo=UTC)
    event = _event(occurred_at=now)
    with pytest.raises(ValueError, match="at least 32 bytes"):
        minimize_audit_event(event, secret=b"short", now=now, retention_days=90)
