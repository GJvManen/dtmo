from pathlib import Path

import pytest

from dtmo.auth.policy import Principal, Role
from dtmo.sources import validate_source_url


ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "backend/dtmo/admin_sources.py"
UI = ROOT / "backend/dtmo/admin_ui.py"
MIGRATION = ROOT / "database/migrations/versions/0007_source_registry.py"
MAIN = ROOT / "backend/dtmo/main.py"


def test_source_url_requires_public_https_shape() -> None:
    assert validate_source_url("https://example.org/feed.json") == "https://example.org/feed.json"
    for unsafe in (
        "http://example.org/feed.json",
        "https://localhost/feed.json",
        "https://service.internal/feed.json",
        "https://127.0.0.1/feed.json",
        "https://10.0.0.1/feed.json",
        "https://user:pass@example.org/feed.json",
        "https://example.org:8443/feed.json",
    ):
        with pytest.raises(ValueError):
            validate_source_url(unsafe)


def test_admin_registry_requires_human_admin_and_manage_connector_permission() -> None:
    text = API.read_text(encoding="utf-8")
    assert "Permission.MANAGE_CONNECTORS" in text
    assert "Role.ADMIN not in principal.roles" in text
    assert "principal.is_service_account" in text
    assert "source registry changes require a human admin role" in text
    assert "append_persistent_audit_event" in text
    assert 'action="source.create"' in text
    assert 'action="source.update"' in text


def test_secret_values_are_references_only() -> None:
    text = (ROOT / "backend/dtmo/sources.py").read_text(encoding="utf-8")
    assert 'startswith(("vault://", "secret://", "env://"))' in text
    assert "never a raw secret" in text


def test_registry_migration_is_after_connector_replay() -> None:
    text = MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "0007_source_registry"' in text
    assert 'down_revision: str | None = "0006_connector_replay"' in text
    assert '"source_definitions"' in text
    assert "ck_source_interval" in text
    assert "ck_source_type" in text


def test_admin_workspace_is_wired_and_accessible() -> None:
    main = MAIN.read_text(encoding="utf-8")
    ui = UI.read_text(encoding="utf-8")
    assert "app.include_router(admin_sources_router)" in main
    assert "app.include_router(admin_ui_router)" in main
    assert 'version="16.0.0rc8"' in main
    assert 'href="#content"' in ui
    assert 'role="status"' in ui
    assert "/api/v1/admin/sources" in ui
    assert "sessionStorage" in ui


def test_service_account_cannot_be_made_human_admin() -> None:
    with pytest.raises(ValueError):
        Principal(subject="service:connector", roles=frozenset({Role.SERVICE_ACCOUNT, Role.ADMIN}))
