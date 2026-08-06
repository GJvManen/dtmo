from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from dtmo.audit.chain import AuditDecision
from dtmo.audit.store import append_persistent_audit_event

from .policy import Principal
from .token_state import TokenStateStore


@dataclass(frozen=True, slots=True)
class RevocationResult:
    jti: str
    expires_at: datetime
    audit_event_id: UUID


def revoke_token_with_audit(
    session: Session,
    *,
    store: TokenStateStore,
    principal: Principal,
    jti: str,
    expires_at: datetime,
    reason: str,
    request_id: str,
    now: datetime | None = None,
) -> RevocationResult:
    token_id = jti.strip()
    rationale = reason.strip()
    correlation_id = request_id.strip()
    current = now or datetime.now(UTC)
    expiry = expires_at.astimezone(UTC)
    if not token_id:
        raise ValueError("token identifier is required")
    if not rationale:
        raise ValueError("revocation reason is required")
    if not correlation_id:
        raise ValueError("request ID is required")
    if expiry <= current.astimezone(UTC):
        raise ValueError("token expiry must be in the future")

    store.revoke(token_id, expires_at=expiry, now=current)
    event = append_persistent_audit_event(
        session,
        principal=principal.subject,
        principal_type="human",
        action="token.revoke",
        resource=f"token:jti:{token_id}",
        decision=AuditDecision.ALLOW,
        request_id=correlation_id,
        provenance_reference=f"reason:{rationale}",
    )
    return RevocationResult(jti=token_id, expires_at=expiry, audit_event_id=event.event_id)
