from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_analysis_primary_flow_discovers_canonical_targets_and_keeps_uuid_secondary() -> None:
    workspace = read("frontend/src/AnalysisWorkspace.tsx")
    assert "Canonical target discovery" in workspace
    assert "Select intelligence object" in workspace
    assert "'/api/v1/command-center'" in workspace
    assert "Recent canonical intelligence targets" in workspace
    assert "Advanced deep link / troubleshooting" in workspace
    assert "Canonical intelligence item ID" in workspace
    assert "No empty-object or platform-health conclusion is inferred" in workspace


def test_ioc_pivot_carries_selected_observable_without_auto_execution() -> None:
    ioc = read("frontend/src/IocExplorerWorkspace.tsx")
    analysis = read("frontend/src/AnalysisWorkspace.tsx")
    assert "observable_type: record.observable_type" in ioc
    assert "observable_value: record.observable_value" in ioc
    assert "Enrich / analyze selected IOC" in ioc
    assert "initial.get('observable_type')" in analysis
    assert "initial.get('observable_value')" in analysis
    assert "Run IntelOwl" in analysis
    assert "Run Cortex" in analysis
    assert "review:intelligence required" in analysis
    assert "No responder authority" in analysis


def test_threat_intelligence_detail_has_direct_analysis_pivot_without_auto_execution() -> None:
    intelligence = read("frontend/src/UnifiedIntelligenceWorkspace.tsx")
    analysis = read("frontend/src/AnalysisWorkspace.tsx")
    assert "Continue investigation" in intelligence
    assert "Analyze &amp; enrich" in intelligence
    assert "/workbench/analysis?item=${encodeURIComponent(detail.id)}" in intelligence
    assert "never executes an analyzer automatically" in intelligence
    assert "execution still requires <code>review:intelligence</code>" in intelligence
    assert "initial.get('item')" in analysis
    assert "/api/v1/analysis/items/${encodeURIComponent(normalized)}/history" in analysis


def test_analysis_exposes_persisted_history_and_cortex_result_without_inferred_authority() -> None:
    workspace = read("frontend/src/AnalysisWorkspace.tsx")
    api = read("backend/dtmo/intelowl_execution.py")
    assert "IntelOwl history" in workspace
    assert "Cortex history" in workspace
    assert "Persisted result" in workspace
    assert "JSON.stringify(record.report, null, 2)" in workspace
    assert "External share: no · Local compromise proven: no" in workspace
    assert "Enrichment is evidence, not a verdict" in workspace
    assert '"/api/v1/analysis/items/{item_id}/history"' in api
    assert '"/api/v1/analysis/items/{item_id}/cortex"' in api


def test_successful_cortex_mutation_commits_before_history_reload() -> None:
    api = read("backend/dtmo/intelowl_execution.py")
    persist = api.index("record = await CortexAnalysisRepository(session).persist(")
    commit = api.index("await session.commit()", persist)
    response = api.index("return _cortex_response(record)", commit)
    assert persist < commit < response


def test_analysis_recovery_documentation_matches_functional_boundary() -> None:
    guide = read("docs/user/INTEGRATED_ANALYSIS_WORKSPACE.md")
    assert "without requiring opaque UUID copy/paste as the primary workflow" in guide
    assert "Threat Intelligence object detail" in guide
    assert "does not execute an analyzer automatically" in guide
    assert "stored Cortex result payloads" in guide
    assert "committed before the successful 201 response" in guide
    assert "Phase 11.10q remains blocked until the owner functional retest" in guide
