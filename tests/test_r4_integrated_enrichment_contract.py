from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_persisted_observables_are_presented_from_governed_enrichment_evidence():
    ioc = read("frontend/src/IocExplorerWorkspace.tsx")
    backend = read("backend/dtmo/intelowl_execution.py")
    assert "Persisted observables from governed enrichment runs" in ioc
    assert "No text-derived or synthetic IOCs" in ioc
    assert '"/api/v1/iocs"' in backend
    assert "IOC inventory contains observables persisted from governed DTMO enrichment executions only" in backend


def test_object_and_ioc_context_open_same_governed_analysis_workspace():
    intelligence = read("frontend/src/UnifiedIntelligenceWorkspace.tsx")
    ioc = read("frontend/src/IocExplorerWorkspace.tsx")
    analysis = read("frontend/src/AnalysisWorkspace.tsx")
    assert "/workbench/analysis?item=${encodeURIComponent(detail.id)}" in intelligence
    assert "observable_type: record.observable_type" in ioc
    assert "observable_value: record.observable_value" in ioc
    assert "initial.get('item')" in analysis
    assert "initial.get('observable_type')" in analysis
    assert "initial.get('observable_value')" in analysis


def test_enrichment_history_is_durable_and_reloaded_after_execution():
    analysis = read("frontend/src/AnalysisWorkspace.tsx")
    backend = read("backend/dtmo/intelowl_execution.py")
    assert "/api/v1/analysis/items/${encodeURIComponent(normalized)}/history" in analysis
    assert "await loadHistory(itemId)" in analysis
    assert "IntelOwl history" in analysis
    assert "Cortex history" in analysis
    assert '"/api/v1/analysis/items/{item_id}/history"' in backend


def test_r4_preserves_human_authority_and_server_side_policy_boundaries():
    analysis = read("frontend/src/AnalysisWorkspace.tsx")
    backend = read("backend/dtmo/intelowl_execution.py")
    assert "review:intelligence required" in analysis
    assert "No responder authority" in analysis
    assert "Enrichment is evidence, not a verdict" in analysis
    assert "Permission.REVIEW_INTELLIGENCE" in backend
    assert "feature_intelowl_enrichment" in backend
    assert "feature_cortex_analysis" in backend
    assert "do not authorize external sharing" in backend
