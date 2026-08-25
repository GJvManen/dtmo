from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
BACKEND = ROOT / "backend/dtmo/admin_center.py"
READINESS = ROOT / "backend/dtmo/integration_readiness.py"


def test_thehive_organization_scope_is_configurable_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")

    assert "TheHive organization scope" in workspace
    assert "thehive_organization" in workspace
    assert "thehive_organization" in backend
    assert 'integration_id in {"ail", "intelowl", "cortex", "opencti", "thehive"}' in backend
    assert "TheHive organization scope is only valid for the TheHive integration" in backend
    assert 'integration_id == "thehive" and not settings.thehive_organization.strip()' in readiness


def test_thehive_policy_uses_shared_fail_closed_readiness() -> None:
    backend = BACKEND.read_text(encoding="utf-8")
    assert "integration_readiness(settings)" in backend
    assert '"thehive_organization": settings.thehive_organization if integration_id == "thehive" else ""' in backend
    assert 'values["thehive_organization"] = settings.thehive_organization' in backend


def test_thehive_credential_remains_server_side() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    assert "Credential (write-only)" in workspace
    assert "Credentials and authorization policy remain server-side." in workspace
