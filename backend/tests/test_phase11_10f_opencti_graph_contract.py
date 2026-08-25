from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_opencti_graph_workspace_package_exists() -> None:
    for path in (
        "backend/dtmo/opencti_workspace.py",
        "frontend/src/OpenCTIGraphWorkspace.tsx",
        "frontend/src/opencti-graph.css",
        "backend/tests/test_phase11_10f_opencti_graph_browser.py",
        "docs/architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "docs/user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "docs/qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md",
        ".github/workflows/phase11-opencti-graph-workspace.yml",
    ):
        assert (ROOT / path).is_file(), path


def test_server_api_is_read_only_and_server_authorized() -> None:
    source = read("backend/dtmo/opencti_workspace.py")
    for marker in (
        '"/api/v1/opencti/capabilities"',
        '"/api/v1/opencti/items/{item_id}/graph"',
        '"/api/v1/opencti/entities/{mapping_id}"',
        "Permission.READ_INTELLIGENCE",
        "OpenCTIObjectMapping",
        "OpenCTIMappingRevision",
        'relationship_type="canonical-mapping"',
        'upstream_relationship_topology_persisted: bool = False',
        "must not be inferred",
        "does not prove local exposure or compromise",
    ):
        assert marker in source, marker
    assert "@router.post" not in source
    assert "@router.put" not in source
    assert "@router.delete" not in source


def test_existing_opencti_persistence_authority_boundaries_remain_intact() -> None:
    persistence = read("backend/dtmo/persistence/opencti.py")
    for marker in (
        "ck_opencti_mapping_no_share_authority",
        "ck_opencti_mapping_no_compromise_proof",
        "uq_opencti_mapping_revision_hash",
        "external_share_authorized=False",
        "local_compromise_proven=False",
    ):
        assert marker in persistence, marker


def test_frontend_uses_dtmo_api_only_and_routes_graph_workspace() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/OpenCTIGraphWorkspace.tsx")
    assert "OpenCTIGraphWorkspace" in app
    assert 'path="/intelligence/graph" element={<OpenCTIGraphWorkspace />}' in app
    for marker in (
        "/api/v1/opencti/capabilities",
        "/api/v1/opencti/items/",
        "/api/v1/opencti/entities/",
        "Roots are discovered from canonical DTMO persistence",
        "Selecting a root reads only DTMO-persisted graph mappings",
        "Relationship topology",
        "Graph presence is context, not a verdict",
    ):
        assert marker in workspace, marker
    for forbidden in ("opencti_api_token", "Authorization: Bearer", "https://opencti", "/graphql"):
        assert forbidden not in workspace, forbidden


def test_graph_never_promotes_configuration_or_presence_to_operational_proof() -> None:
    source = read("backend/dtmo/opencti_workspace.py") + read("frontend/src/OpenCTIGraphWorkspace.tsx")
    for marker in (
        "runtime_health_claim",
        "not inferred",
        "not persisted",
        "external_share_authority",
        "local_compromise_proof",
        "not authorized",
        "not proven",
    ):
        assert marker.lower() in source.lower(), marker
