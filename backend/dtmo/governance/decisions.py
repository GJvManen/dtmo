from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from dtmo.audit import AuditDecision
from dtmo.audit.store import append_persistent_audit_event
from dtmo.auth.policy import Principal, require_separate_share_approval
from dtmo.persistence.models import IntelligenceItem


class GovernedDecisionError(RuntimeError):
    """Raised when a governed intelligence transition cannot be completed."""


@dataclass(frozen=True, slots=True)
class GovernedDecisionResult:
    item_id: UUID
    review_status: str
    share_approved: bool
    audit_event_id: UUID


def review_intelligence(
    session: Session,
    *,
    item_id: UUID,
    principal: Principal,
    request_id: str,
) -> GovernedDecisionResult:
    item = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.id == item_id).with_for_update()
    )
    if item is None:
        raise GovernedDecisionError("intelligence item not found")
    if principal.is_service_account:
        raise GovernedDecisionError("service accounts cannot review intelligence")

    item.review_status = "reviewed"
    item.metadata_json = {**item.metadata_json, "reviewed_by": principal.subject}
    event = append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="intelligence.review",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.ALLOW,
        request_id=request_id,
        provenance_reference=item.canonical_url,
    )
    session.flush()
    return GovernedDecisionResult(
        item_id=item.id,
        review_status=item.review_status,
        share_approved=item.share_approved,
        audit_event_id=event.event_id,
    )


def approve_intelligence_sharing(
    session: Session,
    *,
    item_id: UUID,
    principal: Principal,
    request_id: str,
) -> GovernedDecisionResult:
    item = session.scalar(
        select(IntelligenceItem).where(IntelligenceItem.id == item_id).with_for_update()
    )
    if item is None:
        raise GovernedDecisionError("intelligence item not found")
    if item.review_status != "reviewed":
        raise GovernedDecisionError("intelligence must be reviewed before sharing approval")

    reviewed_by = str(item.metadata_json.get("reviewed_by", ""))
    try:
        require_separate_share_approval(principal, reviewed_by=reviewed_by)
    except PermissionError as exc:
        append_persistent_audit_event(
            session,
            principal=principal.subject,
            principal_type="service_account" if principal.is_service_account else "human",
            action="intelligence.share_approve",
            resource=f"intelligence:{item.id}",
            decision=AuditDecision.DENY,
            request_id=request_id,
            provenance_reference=item.canonical_url,
        )
        session.flush()
        raise GovernedDecisionError(str(exc)) from exc

    item.share_approved = True
    item.metadata_json = {**item.metadata_json, "share_approved_by": principal.subject}
    event = append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="intelligence.share_approve",
        resource=f"intelligence:{item.id}",
        decision=AuditDecision.ALLOW,
        request_id=request_id,
        provenance_reference=item.canonical_url,
    )
    session.flush()
    return GovernedDecisionResult(
        item_id=item.id,
        review_status=item.review_status,
        share_approved=item.share_approved,
        audit_event_id=event.event_id,
    )
