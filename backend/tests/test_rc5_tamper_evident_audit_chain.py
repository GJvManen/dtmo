from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID

import pytest

from dtmo.audit import AuditDecision, append_audit_event, verify_audit_chain


def _chain() -> list:
    first = append_audit_event(
        [],
        principal="analyst@example.test",
        principal_type="human",
        action="intelligence.review",
        resource="intelligence:item-1",
        decision=AuditDecision.ALLOW,
        request_id="request-1",
        provenance_reference="source:1",
        occurred_at=datetime(2026, 8, 6, 12, 0, tzinfo=UTC),
        event_id=UUID("00000000-0000-0000-0000-000000000001"),
    )
    second = append_audit_event(
        [first],
        principal="publisher@example.test",
        principal_type="human",
        action="intelligence.share_approve",
        resource="intelligence:item-1",
        decision=AuditDecision.ALLOW,
        request_id="request-2",
        provenance_reference="source:1",
        occurred_at=datetime(2026, 8, 6, 12, 1, tzinfo=UTC),
        event_id=UUID("00000000-0000-0000-0000-000000000002"),
    )
    return [first, second]


def test_valid_chain_verifies_and_is_deterministic() -> None:
    events = _chain()
    assert verify_audit_chain(events) == (True, None)
    rebuilt = append_audit_event(
        [],
        principal=events[0].principal,
        principal_type=events[0].principal_type,
        action=events[0].action,
        resource=events[0].resource,
        decision=events[0].decision,
        request_id=events[0].request_id,
        provenance_reference=events[0].provenance_reference,
        occurred_at=events[0].occurred_at,
        event_id=events[0].event_id,
    )
    assert rebuilt.event_hash == events[0].event_hash


@pytest.mark.parametrize(
    "mutated",
    [
        lambda event: replace(event, principal="attacker@example.test"),
        lambda event: replace(event, decision=AuditDecision.DENY),
        lambda event: replace(event, occurred_at=event.occurred_at + timedelta(seconds=1)),
        lambda event: replace(event, provenance_reference="source:tampered"),
    ],
)
def test_payload_tampering_is_detected(mutated: object) -> None:
    events = _chain()
    events[0] = mutated(events[0])  # type: ignore[operator]
    valid, reason = verify_audit_chain(events)
    assert not valid
    assert reason == "event hash mismatch at position 0"


def test_removed_or_reordered_record_breaks_chain() -> None:
    events = _chain()
    assert verify_audit_chain(events[1:]) == (False, "broken previous_hash at position 0")
    assert verify_audit_chain(list(reversed(events))) == (False, "broken previous_hash at position 0")


def test_duplicate_event_identifier_is_detected() -> None:
    events = _chain()
    duplicate = replace(events[1], event_id=events[0].event_id)
    valid, reason = verify_audit_chain([events[0], duplicate])
    assert not valid
    assert reason == "duplicate event_id at position 1"


def test_required_audit_fields_fail_closed() -> None:
    with pytest.raises(ValueError, match="required"):
        append_audit_event(
            [],
            principal="",
            principal_type="human",
            action="login",
            resource="session",
            decision=AuditDecision.RECORD,
            request_id="request-3",
        )
