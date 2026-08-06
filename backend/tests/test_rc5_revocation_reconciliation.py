from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from dtmo.auth.policy import Principal, Role
from dtmo.auth.reconciliation import (
    RevocationReconciliationError,
    reconcile_token_revocations,
)
from dtmo.auth.revocation import revoke_token_with_audit
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.models import Base


class MemoryRevocationState:
    def __init__(self) -> None:
        self.revoked: dict[str, datetime] = {}

    def is_revoked(self, jti: str) -> bool:
        return jti in self.revoked

    def revoke(
        self,
        jti: str,
        *,
        expires_at: datetime,
        now: datetime | None = None,
    ) -> None:
        del now
        self.revoked[jti] = expires_at


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def _persist_revocation(
    session: Session,
    store: MemoryRevocationState,
    *,
    jti: str,
    expires_at: datetime,
    now: datetime,
) -> None:
    revoke_token_with_audit(
        session,
        store=store,
        principal=Principal("ciso@example.test", frozenset({Role.CISO})),
        jti=jti,
        expires_at=expires_at,
        reason="credential compromise",
        request_id=f"request-{jti}",
        now=now,
    )
    session.commit()


def test_reconciliation_restores_missing_active_revocation() -> None:
    now = datetime(2026, 8, 6, 12, 30, tzinfo=UTC)
    expires_at = now + timedelta(minutes=30)
    store = MemoryRevocationState()
    with _session() as session:
        _persist_revocation(session, store, jti="token-1", expires_at=expires_at, now=now)
        store.revoked.clear()

        report = reconcile_token_revocations(session, store=store, now=now)

    assert report.scanned == 1
    assert report.restored == 1
    assert report.already_present == 0
    assert store.revoked == {"token-1": expires_at}


def test_reconciliation_is_idempotent_for_present_revocation() -> None:
    now = datetime(2026, 8, 6, 12, 30, tzinfo=UTC)
    expires_at = now + timedelta(minutes=30)
    store = MemoryRevocationState()
    with _session() as session:
        _persist_revocation(session, store, jti="token-2", expires_at=expires_at, now=now)
        report = reconcile_token_revocations(session, store=store, now=now)

    assert report.restored == 0
    assert report.already_present == 1


def test_reconciliation_does_not_restore_expired_revocation() -> None:
    issued_at = datetime(2026, 8, 6, 12, 0, tzinfo=UTC)
    expires_at = issued_at + timedelta(minutes=5)
    store = MemoryRevocationState()
    with _session() as session:
        _persist_revocation(
            session,
            store,
            jti="token-expired",
            expires_at=expires_at,
            now=issued_at,
        )
        store.revoked.clear()
        report = reconcile_token_revocations(
            session,
            store=store,
            now=issued_at + timedelta(minutes=10),
        )

    assert report.expired == 1
    assert store.revoked == {}


def test_reconciliation_fails_closed_on_malformed_durable_evidence() -> None:
    now = datetime(2026, 8, 6, 12, 30, tzinfo=UTC)
    store = MemoryRevocationState()
    with _session() as session:
        _persist_revocation(
            session,
            store,
            jti="token-invalid",
            expires_at=now + timedelta(minutes=30),
            now=now,
        )
        record = session.scalar(select(AuditEventRecord))
        assert record is not None
        record.provenance_reference = "not-json"
        session.commit()

        with pytest.raises(RevocationReconciliationError, match="audit chain verification failed"):
            reconcile_token_revocations(session, store=store, now=now)
