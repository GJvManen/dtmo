from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_source_distribution_is_grouped_from_canonical_persistence():
    backend = read("backend/dtmo/command_center.py")
    assert '"source_distribution": []' in backend
    assert "select(IntelligenceItem.source_id, func.count())" in backend
    assert ".group_by(IntelligenceItem.source_id)" in backend
    assert '"source_id": str(source_id)' in backend


def test_visual_analytics_renders_source_distribution_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "source_distribution: SourcePoint[]" in frontend
    assert 'title="Source contribution"' in frontend
    assert 'labelKey="Source"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_source_analytics_fail_closed_and_preserve_authority_boundaries():
    backend = read("backend/dtmo/command_center.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "data_state = \"unavailable\"" in backend
    assert "trends = _empty_trends()" in backend
    assert "No attributable values are synthesized" in frontend
    assert "does not prove source reachability" in frontend
    assert "sharing approval or publication authority" in frontend
