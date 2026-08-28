from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_enrichment_status_is_grouped_from_canonical_persistence():
    backend = read("backend/dtmo/command_center.py")
    assert '"enrichment_status_distribution": []' in backend
    assert "select(IntelOwlEnrichmentRecord.status, func.count())" in backend
    assert ".group_by(IntelOwlEnrichmentRecord.status)" in backend
    assert '"status": str(status)' in backend


def test_visual_analytics_renders_enrichment_status_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "enrichment_status_distribution: EnrichmentStatusPoint[]" in frontend
    assert 'title="Enrichment status"' in frontend
    assert 'labelKey="Status"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_enrichment_analytics_fail_closed_and_preserve_authority_boundaries():
    backend = read("backend/dtmo/command_center.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert 'data_state = "unavailable"' in backend
    assert "trends = _empty_trends()" in backend
    assert "No attributable values are synthesized" in frontend
    assert "does not prove live connectivity" in frontend
    assert "does not prove local exposure" in frontend
    assert "sharing approval or publication authority" in frontend
    assert "analyzer correctness" in frontend
