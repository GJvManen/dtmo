from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
MAIN = ROOT / "frontend/src/main.tsx"
BACKEND = ROOT / "backend/dtmo/admin_center.py"


def test_canonical_administration_route_is_not_a_generic_empty_foundation() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    main = MAIN.read_text(encoding="utf-8")
    assert "AdministrationWorkspace" in main
    assert 'path="/administration"' in main
    assert "<AdministrationWorkspace />" in main
    assert "Framework integrations" in workspace
    assert "Runtime configuration" in workspace


def test_canonical_administration_uses_same_origin_governed_read_and_patch() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    assert "credentials: 'same-origin'" in workspace
    assert "'/api/v1/admin/integrations'" in workspace
    assert "writeJson<IntegrationRow>(`/api/v1/admin/integrations/${encodeURIComponent(id)}`, 'PATCH'" in workspace
    assert "/api/v1/admin/integrations/${encodeURIComponent(id)}" in workspace
    assert 'require_permission(Permission.MANAGE_CONNECTORS)' in backend
    assert '@router.patch("/api/v1/admin/integrations/{integration_id}")' in backend


def test_browser_never_receives_or_edits_integration_secret_values() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    assert "credential_configured" in workspace
    assert "Credentials remain server-side and are never returned by this API." in backend
    assert "api_key" not in workspace.lower()
    assert "api_token" not in workspace.lower()
    assert "password" not in workspace.lower()
