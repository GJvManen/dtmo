from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_phase11_10g_package_exists() -> None:
    for path in (
        "backend/dtmo/misp_sharing_workspace.py",
        "frontend/src/MispSharingWorkspace.tsx",
        "frontend/src/misp-sharing.css",
    ):
        assert (ROOT / path).is_file(), path


def test_sharing_state_is_read_authorized_and_does_not_claim_runtime_health() -> None:
    api = read("backend/dtmo/misp_sharing_workspace.py")
    assert 'router = APIRouter(prefix="/sharing"' in api
    assert '@router.get("/items/{item_id}")' in api
    assert "Permission.READ_INTELLIGENCE" in api
    assert '"runtime_health_claim": False' in api
    assert '"publication_authority": False' in api
    assert '"synchronization_authority": False' in api
    assert "Configuration does not prove live MISP health" in api


def test_existing_human_authority_separation_remains_server_side() -> None:
    policy = read("backend/dtmo/auth/policy.py")
    decisions = read("backend/dtmo/governance/decisions.py")
    routes = read("backend/dtmo/api/routes.py")
    for marker in (
        'SHARE_APPROVE = "approve:share"',
        "require_separate_share_approval",
        "share approval must be performed by a different principal",
        "service accounts cannot approve external sharing",
    ):
        assert marker in policy
    assert "require_separate_share_approval(principal, reviewed_by=reviewed_by)" in decisions
    assert 'metadata_json = {**item.metadata_json, "reviewed_by": principal.subject}' in decisions
    assert 'metadata_json = {**item.metadata_json, "share_approved_by": principal.subject}' in decisions
    assert '@router.post("/intelligence/{item_id}/review")' in routes
    assert "Permission.REVIEW_INTELLIGENCE" in routes
    assert '@router.post("/intelligence/{item_id}/share-approval")' in routes
    assert "Permission.SHARE_APPROVE" in routes


def test_misp_export_remains_unpublished_replay_protected_and_restriction_aware() -> None:
    export_api = read("backend/dtmo/misp_export_api.py")
    governance = read("backend/dtmo/governance/misp_export.py")
    assert "router.include_router(misp_sharing_workspace_router)" in export_api
    assert '@router.post("/intelligence/{item_id}/misp-export")' in export_api
    assert "Permission.SHARE_APPROVE" in export_api
    assert "never publishes" in export_api
    assert '"published": False' in governance
    assert "authoritative MISP distribution cannot be changed on re-export" in governance
    assert "requested TLP is less restrictive than authoritative source TLP" in governance
    assert "MISP export replay blocked for this canonical revision" in governance
    assert 'record["status"] = "uncertain"' in governance


def test_canonical_workbench_uses_dtmo_apis_only_and_has_no_publish_control() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/MispSharingWorkspace.tsx")
    assert "import { MispSharingWorkspace }" in app
    assert "workspace.path === '/sharing'" in app
    assert "<MispSharingWorkspace />" in app
    for marker in (
        "/api/v1/ui/session",
        "/api/v1/sharing/items/",
        "/api/v1/intelligence/",
        "/review",
        "/share-approval",
        "/misp-export",
        "11.10g MISP Sharing",
        "reviewed_by === session.subject",
        "There is no publish or synchronize control.",
    ):
        assert marker in workspace
    for forbidden in (
        "misp_api_key",
        "Authorization: Bearer",
        "Authorization',",
        "https://misp",
        "/events/add",
        "publish-event",
        "synchronize-event",
    ):
        assert forbidden not in workspace


def test_11_10g_does_not_promote_configuration_or_transfer_to_authority() -> None:
    workspace = read("frontend/src/MispSharingWorkspace.tsx")
    for marker in (
        "Runtime health: not inferred",
        "Publication authority: no",
        "Synchronization authority: no",
        "Human authority required",
        "Approver must be a different human principal from the reviewer",
        "No approval, export or MISP-health conclusion is inferred",
    ):
        assert marker in workspace
