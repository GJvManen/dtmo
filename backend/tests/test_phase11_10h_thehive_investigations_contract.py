from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_phase11_10h_package_exists() -> None:
    for path in (
        "backend/dtmo/thehive_handoff.py",
        "frontend/src/InvestigationsWorkspace.tsx",
        "frontend/src/investigations.css",
    ):
        assert (ROOT / path).is_file(), path


def test_investigation_state_is_read_authorized_and_evidence_bounded() -> None:
    api = read("backend/dtmo/thehive_handoff.py")
    assert '"/items/{item_id}/investigation"' in api
    assert "Permission.READ_INTELLIGENCE" in api
    assert "TheHiveHandoffRepository(session).list_for_item(item_id)" in api
    assert "runtime_health_claim=False" in api
    assert "upstream_case_readback_supported=False" in api
    assert "alerts_tasks_timeline_persisted=False" in api
    assert "external_share_authority=False" in api
    assert "local_compromise_proof=False" in api
    assert "Alerts, tasks and case timeline" in api


def test_case_mutation_remains_existing_human_authorized_server_side_boundary() -> None:
    api = read("backend/dtmo/thehive_handoff.py")
    policy = read("backend/dtmo/auth/policy.py")
    persistence = read("backend/dtmo/persistence/thehive.py")
    for marker in (
        '@router.post(\n    "/items/{item_id}/cases"',
        "Permission.CASE_HANDOFF",
        "service accounts cannot authorize TheHive case handoff",
        "TheHive handoff requires canonical provenance",
        "manual reconciliation required",
        '"human_authorized": True',
        '"external_share_authorized": False',
        '"local_compromise_proven": False',
    ):
        assert marker in api
    assert 'CASE_HANDOFF = "handoff:case"' in policy
    assert "ck_thehive_handoff_no_share_authority" in persistence
    assert "ck_thehive_handoff_no_compromise_proof" in persistence
    assert "already {existing.status}; reconciliation required" in persistence


def test_canonical_investigations_workspace_uses_dtmo_api_only() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/InvestigationsWorkspace.tsx")
    assert "import { InvestigationsWorkspace }" in app
    assert "workspace.path === '/investigations'" in app
    assert "<InvestigationsWorkspace />" in app
    for marker in (
        "/api/v1/thehive/items/",
        "/investigation",
        "/cases",
        "11.10h TheHive Investigations",
        "Human case authority required",
        "Manual reconciliation required",
        "Create TheHive case handoff",
        "Runtime health: not inferred",
        "External share authority: no",
        "Local compromise proof: no",
    ):
        assert marker in workspace
    for forbidden in (
        "thehive_api_token",
        "Authorization: Bearer",
        "X-Organisation",
        "https://thehive",
        "/api/v1/case",
        "execute responder",
        "auto-create",
    ):
        assert forbidden not in workspace


def test_workspace_does_not_fabricate_unpersisted_thehive_objects() -> None:
    workspace = read("frontend/src/InvestigationsWorkspace.tsx")
    for marker in (
        "Alerts:</strong> not persisted/read back",
        "Tasks:</strong> not persisted/read back",
        "Case timeline:</strong> not persisted/read back",
        "Responders:</strong> no execution authority",
        "does not prove subsequent upstream case state or action",
    ):
        assert marker in workspace
