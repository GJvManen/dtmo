from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "OpenCTIGraphWorkspace.tsx"


def test_knowledge_graph_discovers_roots_from_canonical_persistence() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "'/api/v1/command-center'" in source
    assert "Recent intelligence roots" in source
    assert "Recent canonical graph roots" in source
    assert "loadGraphFor(root.id)" in source
    assert "without knowing an internal UUID" in source


def test_manual_uuid_is_secondary_not_primary_operator_flow() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "Advanced: open a known canonical item ID" in source
    assert "Secondary deep-link/troubleshooting path only" in source
    assert "Normal operator discovery is provided above" in source


def test_graph_discovery_preserves_evidence_boundaries() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")
    assert "the browser does not query OpenCTI directly" in source
    assert "No upstream-health or absence conclusion is inferred" in source
    assert "OpenCTI entity-to-entity relationships are not drawn unless they are durably persisted by DTMO" in source
    assert "Graph presence is context, not a verdict" in source
