from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from starlette.requests import Request

from dtmo.auth import dependencies
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.auth.revocation import revoke_token_with_audit
from dtmo.persistence.audit_models import AuditEventRecord
from dtmo.persistence.models import Base


class RecordingTokenStore:
    def __init__(self) -> None:
        self.revocations: list[tuple[str, datetime]] = []

    def revoke(
        self,
        jti: str,
        *,
        expires_at: datetime,
        now: datetime | None = None,
    ) -> None:
        del now
        self.revocations.append((jti, expires_at))


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_ciso_can_revoke_token_and_append_allow_audit_event() -> None:
    store = RecordingTokenStore()
    principal = Principal("ciso@example.test", frozenset({Role.CISO}))
    expires_at = datetime.now(UTC) + timedelta(minutes=10)
    with _session() as session:
        result = revoke_token_with_audit(
            session,
            store=store,
            principal=principal,
            jti="token-123",
            expires_at=expires_at,
            reason="suspected credential theft",
            request_id="request-123",
        )
        session.commit()
        record = session.scalar(select(AuditEventRecord))

    assert principal.can(Permission.REVOKE_TOKENS)
    assert store.revocations == [("token-123", expires_at)]
    assert record is not None
    assert record.event_id == result.audit_event_id
    assert record.action == "token.revoke"
    assert record.decision == "allow"
    assert record.request_id == "request-123"


def test_revocation_rejects_expired_target_without_state_change() -> None:
    store = RecordingTokenStore()
    principal = Principal("admin@example.test", frozenset({Role.ADMIN}))
    with _session() as session, pytest.raises(ValueError, match="expiry must be in the future"):
        revoke_token_with_audit(
            session,
            store=store,
            principal=principal,
            jti="token-123",
            expires_at=datetime.now(UTC) - timedelta(seconds=1),
            reason="expired already",
            request_id="request-123",
        )
    assert store.revocations == []


@pytest.mark.asyncio
async def test_permission_denial_invokes_audit_writer_before_403(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    async def fake_persist(**kwargs: object) -> None:
        captured.update(kwargs)

    monkeypatch.setattr(dependencies, "_persist_authorization_denial", fake_persist)
    request = Request({"type": "http", "method": "GET", "path": "/api/v1/intelligence/search", "headers": []})
    principal = Principal("analyst@example.test", frozenset({Role.ANALYST}))
    dependency = dependencies.require_permission(Permission.READ_AUDIT)

    with pytest.raises(HTTPException) as exc_info:
        await dependency(request=request, principal=principal, request_id="request-denied")

    assert exc_info.value.status_code == 403
    assert captured["principal"] == principal
    assert captured["permission"] is Permission.READ_AUDIT
    assert captured["resource"] == "/api/v1/intelligence/search"
    assert captured["request_id"] == "request-denied"
