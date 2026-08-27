from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "frontend/src/main.tsx"
CONSOLE = ROOT / "frontend/src/AdministrationConsole.tsx"
WORKSPACE = ROOT / "frontend/src/AdministrationSecurityAudit.tsx"
ROUTES = ROOT / "backend/dtmo/api/routes.py"
AUDITOR = ROOT / "backend/dtmo/auditor_ui.py"


def test_canonical_administration_renders_security_and_audit_without_legacy_navigation() -> None:
    main = MAIN.read_text(encoding="utf-8")
    console = CONSOLE.read_text(encoding="utf-8")
    workspace = WORKSPACE.read_text(encoding="utf-8")
    assert "AdministrationConsole" in main
    assert '<Route path="/administration"' in main
    assert "AdministrationSecurityAudit" in console
    assert "<AdministrationWorkspace />" in console
    assert "<AdministrationSecurityAudit />" in console
    assert "/ui/ciso-security" not in workspace
    assert "/ui/auditor" not in workspace
    assert "No legacy security administration dependency" in workspace


def test_security_administration_uses_server_authorized_same_origin_revocation() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    routes = ROUTES.read_text(encoding="utf-8")
    assert "credentials: 'same-origin'" in workspace
    assert "'/api/v1/security/tokens/revoke'" in workspace
    assert "'X-Request-ID': crypto.randomUUID()" in workspace
    assert "revoke:tokens" in workspace
    assert "service_account" in workspace
    assert '@router.post("/security/tokens/revoke", response_model=TokenRevocationResponse)' in routes
    assert "require_permission(Permission.REVOKE_TOKENS)" in routes
    assert "revoke_token_with_audit" in routes


def test_canonical_audit_projection_remains_read_only_and_permission_guarded() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    auditor = AUDITOR.read_text(encoding="utf-8")
    assert "'/api/v1/audit/events?limit=50'" in workspace
    assert "read:audit" in workspace
    assert "Recent append-only audit evidence" in workspace
    assert "read-only projection" in workspace
    assert '@router.get("/api/v1/audit/events")' in auditor
    assert "require_permission(Permission.READ_AUDIT)" in auditor
    assert '"read_only": True' in auditor


def test_security_audit_ui_does_not_claim_extra_authority_or_expose_credentials() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    lowered = workspace.lower()
    assert "grants no mutation, review, sharing or publication authority" in workspace
    assert "does not expose secrets" in workspace
    assert "api_key" not in lowered
    assert "password" not in lowered
    assert "publication authority" in lowered
