from __future__ import annotations

from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dtmo.audit.store import load_audit_chain
from dtmo.auth.policy import Permission, Principal, Role
from dtmo.persistence.audit_models import AuditEventRecord  # noqa: F401
from dtmo.persistence.models import Base
from dtmo.rbac_admin import (
    MANAGED_HUMAN,
    MANAGED_SERVICE_ACCOUNT,
    ManagedPrincipal,
    ManagedPrincipalStore,
    ManagedRoleAssignment,
    RbacConflictError,
    RbacValidationError,
    _audit,
    validate_roles,
    validate_subject,
)
from dtmo.rc13_administration import extend_console_page
from dtmo.unified_console import _PAGE as BASE_CONSOLE_PAGE

ROOT = Path(__file__).resolve().parents[2]
RBAC_API = ROOT / "backend/dtmo/rbac_admin.py"
MAIN = ROOT / "backend/dtmo/main.py"
MIGRATION = ROOT / "database/migrations/versions/0009_managed_rbac_assignments.py"


def _session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    return Session(engine)


def test_managed_role_contract_preserves_human_machine_boundary() -> None:
    assert validate_roles(MANAGED_HUMAN, [Role.ANALYST, Role.REVIEWER]) == (
        Role.ANALYST,
        Role.REVIEWER,
    )
    assert validate_roles(MANAGED_SERVICE_ACCOUNT, [Role.SERVICE_ACCOUNT]) == (
        Role.SERVICE_ACCOUNT,
    )
    with pytest.raises(RbacValidationError, match="human principals"):
        validate_roles(MANAGED_HUMAN, [Role.SERVICE_ACCOUNT])
    with pytest.raises(RbacValidationError, match="service accounts"):
        validate_roles(MANAGED_SERVICE_ACCOUNT, [Role.SERVICE_ACCOUNT, Role.ADMIN])
    with pytest.raises(RbacValidationError, match="unsupported characters"):
        validate_subject("bad/subject")


def test_store_creates_updates_and_protects_last_managed_admin() -> None:
    with _session() as session:
        store = ManagedPrincipalStore(session)
        first_admin = store.create(
            subject="admin.one@example.test",
            display_name="Admin One",
            principal_type=MANAGED_HUMAN,
            roles=[Role.ADMIN],
            active=True,
            actor="bootstrap-admin",
        )
        assert first_admin.roles == (Role.ADMIN,)
        assert store.active_admin_count() == 1

        with pytest.raises(RbacConflictError, match="last managed admin"):
            store.update(
                first_admin.subject,
                display_name="Admin One",
                active=False,
                roles=[Role.ADMIN],
                actor="bootstrap-admin",
            )

        store.create(
            subject="admin.two@example.test",
            display_name="Admin Two",
            principal_type=MANAGED_HUMAN,
            roles=[Role.ADMIN],
            active=True,
            actor="bootstrap-admin",
        )
        changed = store.update(
            first_admin.subject,
            display_name="Analyst One",
            active=True,
            roles=[Role.ANALYST],
            actor="admin.two@example.test",
        )
        assert changed.roles == (Role.ANALYST,)
        assert store.active_admin_count() == 1
        session.commit()
        assert {state.subject for state in store.list()} == {
            "admin.one@example.test",
            "admin.two@example.test",
        }


def test_rbac_mutation_uses_existing_tamper_evident_audit_chain() -> None:
    with _session() as session:
        actor = Principal(subject="root-admin", roles=frozenset({Role.ADMIN}))
        state = ManagedPrincipalStore(session).create(
            subject="analyst@example.test",
            display_name="Analyst",
            principal_type=MANAGED_HUMAN,
            roles=[Role.ANALYST],
            active=True,
            actor=actor.subject,
        )
        _audit(
            session,
            principal=actor,
            action="rbac.principal.create",
            state=state,
            request_id="rc13-rbac-request",
        )
        session.commit()
        events = load_audit_chain(session)
        assert len(events) == 1
        assert events[0].principal == actor.subject
        assert events[0].action == "rbac.principal.create"
        assert events[0].resource == "principal:analyst@example.test"
        assert events[0].request_id == "rc13-rbac-request"
        assert "roles:analyst" in (events[0].provenance_reference or "")


def test_rbac_api_is_server_side_governed_and_truthful_about_token_effect() -> None:
    text = RBAC_API.read_text(encoding="utf-8")
    assert "Permission.MANAGE_USERS" in text
    assert "Role.ADMIN not in principal.roles" in text
    assert "principal.is_service_account" in text
    assert "administrators cannot change their own managed assignment" in text
    assert "cannot remove or deactivate the last managed admin" in text
    assert 'action="rbac.principal.create"' in text
    assert 'action="rbac.principal.update"' in text
    assert "Production bearer tokens are externally issued" in text
    assert "identity-provider reconciliation or token reissue" in text
    assert Permission.MANAGE_USERS in frozenset(Permission)


def test_rbac_models_are_in_shared_metadata_and_migration_follows_rc12() -> None:
    assert ManagedPrincipal.__table__.metadata is Base.metadata
    assert ManagedRoleAssignment.__table__.metadata is Base.metadata
    text = MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "0009_managed_rbac_assignments"' in text
    assert 'down_revision: str | None = "0008_grafana_reporting_views"' in text
    assert '"managed_principals"' in text
    assert '"managed_role_assignments"' in text
    assert "ck_managed_principal_type" in text


def test_rc13_administration_extension_keeps_one_canonical_console() -> None:
    page = extend_console_page(BASE_CONSOLE_PAGE)
    assert 'data-view-panel="overview"' in page
    assert 'data-view-panel="intelligence"' in page
    assert 'data-view-panel="sources"' in page
    assert 'data-view-panel="analytics"' in page
    assert 'data-view-panel="administration"' in page
    assert 'id="rbac-administration"' in page
    assert 'id="rbac-create-form"' in page
    assert "/ui/rc13-administration.js" in page
    assert 'data-view-panel="governance"' in page

    main = MAIN.read_text(encoding="utf-8")
    assert "app.include_router(rbac_admin_router)" in main
    assert main.index("app.include_router(rc13_administration_router)") < main.index(
        "app.include_router(unified_console_router)"
    )
