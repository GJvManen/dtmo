from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_type_distribution_is_grouped_from_canonical_persistence():
    backend = read("backend/dtmo/command_center.py")
    assert '"type_distribution": []' in backend
    assert "select(IntelligenceItem.item_type, func.count())" in backend
    assert ".group_by(IntelligenceItem.item_type)" in backend
    assert "for item_type in IntelligenceType" in backend
    assert '"item_type": item_type.value' in backend


def test_visual_analytics_renders_type_distribution_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "type_distribution: IntelligenceTypePoint[]" in frontend
    assert 'title="Intelligence type distribution"' in frontend
    assert 'labelKey="Type"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_type_analytics_fail_closed_and_preserve_authority_boundaries():
    backend = read("backend/dtmo/command_center.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "data_state = \"unavailable\"" in backend
    assert "trends = _empty_trends()" in backend
    assert "No attributable values are synthesized" in frontend
    assert "does not prove live connectivity" in frontend
    assert "does not prove local exposure" in frontend
    assert "sharing approval or publication authority" in frontend
