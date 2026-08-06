from __future__ import annotations

from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.audit.store import load_audit_chain, verify_persistent_audit_chain
from dtmo.auth.policy import Principal, Role
from dtmo.governance import (
    GovernedDecisionError,
    approve_intelligence_sharing,
    review_intelligence,
)
from dtmo.intelligence.model import IntelligenceSeverity, IntelligenceType
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.models import Base, IntelligenceItem


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _candidate(session: Session) -> IntelligenceItem:
    item = IntelligenceItem(
        id=uuid4(),
        source_id="test-source",
        external_id="item-1",
        item_type=IntelligenceType.ADVISORY,
        title="Governed item",
        summary="",
        canonical_url="https://example.test/item-1",
        content_hash="a" * 64,
        severity=IntelligenceSeverity.MEDIUM,
        confidence_score=70,
        education_relevance=80,
        review_status="candidate",
        share_approved=False,
        metadata_json={},
    )
    session.add(item)
    session.flush()
    return item


def test_review_and_share_approval_are_atomically_audited() -> None:
    session = _session()
    item = _candidate(session)
    reviewer = Principal("reviewer@example.test", frozenset({Role.REVIEWER}))
    publisher = Principal("publisher@example.test", frozenset({Role.PUBLISHER}))

    review = review_intelligence(
        session,
        item_id=item.id,
        principal=reviewer,
        request_id="request-review",
    )
    approval = approve_intelligence_sharing(
        session,
        item_id=item.id,
        principal=publisher,
        request_id="request-approve",
    )
    session.commit()

    assert review.review_status == "reviewed"
    assert approval.share_approved is True
    assert item.metadata_json["reviewed_by"] == reviewer.subject
    assert item.metadata_json["share_approved_by"] == publisher.subject
    events = load_audit_chain(session)
    assert [event.action for event in events] == [
        "intelligence.review",
        "intelligence.share_approve",
    ]
    assert [event.decision.value for event in events] == ["allow", "allow"]
    assert verify_persistent_audit_chain(session) == (True, None)


def test_same_human_cannot_review_and_approve_and_denial_is_audited() -> None:
    session = _session()
    item = _candidate(session)
    principal = Principal("dual-role@example.test", frozenset({Role.ADMIN}))
    review_intelligence(
        session,
        item_id=item.id,
        principal=principal,
        request_id="request-review",
    )

    with pytest.raises(GovernedDecisionError, match="different principal"):
        approve_intelligence_sharing(
            session,
            item_id=item.id,
            principal=principal,
            request_id="request-denied",
        )

    assert item.share_approved is False
    denied = session.scalars(
        select(AuditEventRecord).where(AuditEventRecord.decision == "deny")
    ).all()
    assert len(denied) == 1
    assert denied[0].request_id == "request-denied"
    assert verify_persistent_audit_chain(session) == (True, None)


def test_rollback_removes_state_change_and_corresponding_audit_event() -> None:
    session = _session()
    item = _candidate(session)
    session.commit()
    reviewer = Principal("reviewer@example.test", frozenset({Role.REVIEWER}))

    review_intelligence(
        session,
        item_id=item.id,
        principal=reviewer,
        request_id="request-rollback",
    )
    session.rollback()

    restored = session.get(IntelligenceItem, item.id)
    assert restored is not None
    assert restored.review_status == "candidate"
    assert load_audit_chain(session) == []
