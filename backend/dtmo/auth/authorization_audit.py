from __future__ import annotations

from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from dtmo.audit.chain import AuditDecision
from dtmo.audit.store import append_persistent_audit_event

from .policy import Permission, Principal


async def record_authorization_denial(
    session: AsyncSession,
    *,
    principal: Principal,
    permission: Permission,
    resource: str,
    request_id: str,
) -> None:
    correlation_id = request_id.strip() or f"generated-{uuid4()}"
    principal_type = "service_account" if principal.is_service_account else "human"
    await session.run_sync(
        lambda sync_session: append_persistent_audit_event(
            sync_session,
            principal=principal.subject,
            principal_type=principal_type,
            action="authorization.check",
            resource=resource,
            decision=AuditDecision.DENY,
            request_id=correlation_id,
            provenance_reference=f"permission:{permission.value}",
        )
    )
