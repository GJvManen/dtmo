from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from sqlalchemy import select
from sqlalchemy.orm import Session

from dtmo.audit.store import verify_persistent_audit_chain
from dtmo.persistence.audit_models import AuditEventRecord


class RevocationState(Protocol):
    def is_revoked(self, jti: str) -> bool: ...

    def revoke(
        self,
        jti: str,
        *,
        expires_at: datetime,
        now: datetime | None = None,
    ) -> None: ...


class RevocationReconciliationError(RuntimeError):
    """Raised when durable revocation evidence cannot be reconciled safely."""


@dataclass(frozen=True, slots=True)
class RevocationReconciliationReport:
    scanned: int
    restored: int
    already_present: int
    expired: int


def _parse_revocation(record: AuditEventRecord) -> tuple[str, datetime]:
    prefix = "token:jti:"
    if not record.resource.startswith(prefix):
        raise RevocationReconciliationError("revocation audit resource is invalid")
    jti = record.resource.removeprefix(prefix).strip()
    if not jti or record.provenance_reference is None:
        raise RevocationReconciliationError("revocation audit evidence is incomplete")
    try:
        payload = json.loads(record.provenance_reference)
        expires_at = datetime.fromisoformat(str(payload["expires_at"]))
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise RevocationReconciliationError("revocation audit provenance is invalid") from exc
    if payload.get("schema") != "token-revocation/v1" or expires_at.tzinfo is None:
        raise RevocationReconciliationError("revocation audit provenance contract is invalid")
    return jti, expires_at.astimezone(UTC)


def reconcile_token_revocations(
    session: Session,
    *,
    store: RevocationState,
    now: datetime | None = None,
) -> RevocationReconciliationReport:
    valid, reason = verify_persistent_audit_chain(session)
    if not valid:
        raise RevocationReconciliationError(f"audit chain verification failed: {reason}")

    current = (now or datetime.now(UTC)).astimezone(UTC)
    records = session.scalars(
        select(AuditEventRecord)
        .where(
            AuditEventRecord.action == "token.revoke",
            AuditEventRecord.decision == "allow",
        )
        .order_by(AuditEventRecord.sequence_number)
    ).all()

    restored = 0
    already_present = 0
    expired = 0
    for record in records:
        jti, expires_at = _parse_revocation(record)
        if expires_at <= current:
            expired += 1
            continue
        if store.is_revoked(jti):
            already_present += 1
            continue
        store.revoke(jti, expires_at=expires_at, now=current)
        restored += 1

    return RevocationReconciliationReport(
        scanned=len(records),
        restored=restored,
        already_present=already_present,
        expired=expired,
    )
