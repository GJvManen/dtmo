from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol
from uuid import UUID

from sqlalchemy.orm import Session

from dtmo.audit.chain import AuditDecision
from dtmo.audit.store import append_persistent_audit_event

from .policy import Principal


class TokenRevoker(Protocol):
    def revoke(
        self,
        jti: str,
        *,
        expires_at: datetime,
        now: datetime | None = None,
    ) -> None: ...


@dataclass(frozen=True, slots=True)
class RevocationResult:
    jti: str
    expires_at: datetime
    audit_event_id: UUID


def revocation_provenance(*, expires_at: datetime, reason: str) -> str:
    return json.dumps(
        {
            "expires_at": expires_at.astimezone(UTC).isoformat(),
            "reason": reason.strip(),
            "schema": "token-revocation/v1",
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def revoke_token_with_audit(
    session: Session,
    *,
    store: TokenRevoker,
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
        provenance_reference=revocation_provenance(expires_at=expiry, reason=rationale),
    )
    return RevocationResult(jti=token_id, expires_at=expiry, audit_event_id=event.event_id)
