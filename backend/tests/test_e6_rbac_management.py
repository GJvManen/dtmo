from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dtmo.audit.store import load_audit_chain
from dtmo.auth.policy import Permission, Principal, ROLE_PERMISSIONS, Role
from dtmo.persistence.audit_models import AuditEventRecord  # noqa: F401
from dtmo.persistence.models import Base
from dtmo.rbac_admin import MANAGED_HUMAN, ManagedPrincipalStore
from dtmo.rbac_management_experience import (
    _PAGE,
    _SCRIPT,
    _audit_governed_assignment,
    _state_summary,
    role_permission_matrix,
    router,
)


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_matrix_contract_is_server_side_policy_truth() -> None:
    assert Permission.MANAGE_USERS in ROLE_PERMISSIONS[Role.ADMIN]
    assert Permission.SHARE_APPROVE in ROLE_PERMISSIONS[Role.PUBLISHER]
    assert Permission.REVIEW_INTELLIGENCE in ROLE_PERMISSIONS[Role.REVIEWER]
    assert Permission.SHARE_APPROVE not in ROLE_PERMISSIONS[Role.REVIEWER]
    assert Permission.REVIEW_INTELLIGENCE not in ROLE_PERMISSIONS[Role.PUBLISHER]
    routes = {route.path for route in router.routes}
    assert "/api/v1/admin/rbac/matrix" in routes
    assert "/api/v1/admin/rbac/principals/{subject}/governed-assignment" in routes
    assert role_permission_matrix.__name__ == "role_permission_matrix"


def test_governed_assignment_audit_records_reason_and_before_after() -> None:
    with _session() as session:
        actor = Principal(subject="admin@example.test", roles=frozenset({Role.ADMIN}))
        store = ManagedPrincipalStore(session)
        before = store.create(
            subject="operator@example.test",
            display_name="Operator",
            principal_type=MANAGED_HUMAN,
            roles=[Role.ANALYST],
            active=True,
            actor=actor.subject,
        )
        after = store.update(
            before.subject,
            display_name="Senior Operator",
            active=True,
            roles=[Role.SENIOR_ANALYST],
            actor=actor.subject,
        )
        _audit_governed_assignment(
            session,
            principal=actor,
            before=before,
            after=after,
            reason="Incident response duty rotation",
            request_id="e6-correlation-123",
        )
        session.commit()
        events = load_audit_chain(session)
        assert len(events) == 1
        event = events[0]
        assert event.action == "rbac.assignment.update"
        assert event.principal == actor.subject
        assert event.request_id == "e6-correlation-123"
        provenance = event.provenance_reference or ""
        assert "reason:Incident response duty rotation" in provenance
        assert "before:" in provenance
        assert "roles=analyst" in provenance
        assert "after:" in provenance
        assert "roles=senior_analyst" in provenance
        assert _state_summary(after) in provenance


def test_e6_console_keeps_single_shell_and_exposes_reasoned_governed_save() -> None:
    assert 'id="e6-rbac-management"' in _PAGE
    assert 'id="rbac-administration"' in _PAGE
    assert 'data-view-panel="administration"' in _PAGE
    assert 'data-view-panel="governance"' in _PAGE
    assert "/ui/rbac-management-experience.js" in _PAGE
    assert "/api/v1/admin/rbac/matrix" in _SCRIPT
    assert "governed-assignment" in _SCRIPT
    assert "Reden voor wijziging" in _SCRIPT
    assert "stopImmediatePropagation" in _SCRIPT
    assert "data-e6-rbac-save" in _SCRIPT


def test_governed_save_reconciles_visible_card_with_server_response() -> None:
    assert "function reconcilePrincipalCard" in _SCRIPT
    assert "reconcilePrincipalCard(card,response.principal)" in _SCRIPT
    assert "badge.textContent = principal.active ? 'Actief' : 'Inactief'" in _SCRIPT
    assert "active.checked = Boolean(principal.active)" in _SCRIPT
    assert "selected.has(input.dataset.rbacRole)" in _SCRIPT


def test_e6_contract_preserves_least_privilege_and_sod_boundaries() -> None:
    source = __import__("inspect").getsource(__import__("dtmo.rbac_management_experience", fromlist=["*"]))
    assert "Service accounts cannot hold human or administrator roles" in source
    assert "Administrators cannot change their own managed assignment" in source
    assert "last active managed human administrator" in source
    assert "review and external-share approval remain separately authorized" in source.lower()
    assert "Role visibility or administration never constitutes review or publication approval" in source
    assert "Field(min_length=3, max_length=500)" in source
