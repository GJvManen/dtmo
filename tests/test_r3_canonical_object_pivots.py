from pathlib import Path


def test_intelligence_detail_exposes_direct_canonical_object_pivots():
    text = Path("frontend/src/UnifiedIntelligenceWorkspace.tsx").read_text(encoding="utf-8")
    for destination in (
        "/workbench/analysis?item=",
        "/workbench/intelligence/graph?item=",
        "/workbench/investigations?item=",
        "/workbench/sharing?item=",
    ):
        assert destination in text
    assert "encodeURIComponent(detail.id)" in text


def test_graph_and_investigation_destinations_reload_server_context_from_item_id():
    graph = Path("frontend/src/OpenCTIGraphWorkspace.tsx").read_text(encoding="utf-8")
    investigations = Path("frontend/src/InvestigationsWorkspace.tsx").read_text(encoding="utf-8")

    assert "new URLSearchParams(window.location.search).get('item')" in graph
    assert "/api/v1/opencti/items/${encodeURIComponent(normalized)}/graph" in graph
    assert "the browser does not query OpenCTI directly" in graph

    assert "new URLSearchParams(window.location.search).get('item')" in investigations
    assert "/api/v1/thehive/items/${encodeURIComponent(id)}/investigation" in investigations
    assert "Mutation remains server-authorized by <code>handoff:case</code>" in investigations


def test_navigation_does_not_claim_or_grant_cross_workspace_authority():
    text = Path("frontend/src/UnifiedIntelligenceWorkspace.tsx").read_text(encoding="utf-8")
    assert "Each destination reloads server-authorized persisted context" in text
    assert "does not create a case or grant responder authority" in text
    assert "grants no review, share approval, export, publication or synchronization authority" in text
