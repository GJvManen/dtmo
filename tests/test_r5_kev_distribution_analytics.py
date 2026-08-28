from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_kev_distribution_is_derived_from_normalized_vulnerability_evidence():
    backend = read("backend/dtmo/vulnerability_analytics.py")
    assert '"status": "known_exploited"' in backend
    assert '"status": "not_known_exploited"' in backend
    assert '"status": "unknown"' in backend
    assert '"kev": kev_distribution' in backend
    assert "if selected:" in backend


def test_visual_analytics_renders_kev_distribution_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "distributions?:" in frontend
    assert "kev?: KevPoint[]" in frontend
    assert 'title="KEV status distribution"' in frontend
    assert 'labelKey="KEV status"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_kev_distribution_preserves_claim_boundaries():
    backend = read("backend/dtmo/vulnerability_analytics.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "does not prove deployment, exploitability, compromise" in backend
    assert "raw object passed the existing integrity boundary" in frontend
    assert "does not prove local deployment, exploitability, compromise or remediation authority" in frontend
