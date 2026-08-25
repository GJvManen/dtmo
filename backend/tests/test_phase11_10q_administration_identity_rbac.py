from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "AdministrationWorkspace.tsx"
RBAC_API = ROOT / "backend" / "dtmo" / "rbac_admin.py"
RBAC_EXPERIENCE = ROOT / "backend" / "dtmo" / "rbac_management_experience.py"


def test_canonical_administration_owns_identity_rbac_control_plane() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "Identity & RBAC" in source
    assert "/api/v1/admin/rbac/roles" in source
    assert "/api/v1/admin/rbac/principals" in source
    assert "/api/v1/admin/rbac/matrix" in source
    assert "/governed-assignment" in source
    assert "manage:users" in source
    assert "Required change reason" in source
    assert "Self-management is server-side blocked" in source
    assert "No legacy administration dependency" in source
    assert 'href="/ui/' not in source


def test_identity_mutations_reuse_server_side_rbac_and_audit_boundaries() -> None:
    api = RBAC_API.read_text(encoding="utf-8")
    governed = RBAC_EXPERIENCE.read_text(encoding="utf-8")
    assert 'router = APIRouter(prefix="/api/v1/admin/rbac"' in api
    assert 'Depends(require_permission(Permission.MANAGE_USERS))' in api
    assert 'cannot remove or deactivate the last managed admin' in api
    assert 'administrators cannot change their own managed assignment' in api
    assert '"/api/v1/admin/rbac/principals/{subject}/governed-assignment"' in governed
    assert 'append_persistent_audit_event' in governed
    assert 'reason: str = Field(min_length=3' in governed
