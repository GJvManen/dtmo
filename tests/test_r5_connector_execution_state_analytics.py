from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_connector_execution_state_uses_canonical_command_center_runtime_observations():
    backend = read("backend/dtmo/command_center.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert '"runtime_observation": run.status if run is not None else None' in backend
    assert '"runtime_health_claim": False' in backend
    assert "runtime_observation?: string | null" in frontend
    assert "if (!integration.runtime_observation) return counts" in frontend
    assert "counts[integration.runtime_observation]" in frontend


def test_visual_analytics_renders_connector_execution_state_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert 'title="Latest connector execution states"' in frontend
    assert 'labelKey="Persisted latest run status"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_connector_execution_state_preserves_evidence_boundaries():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "historical latest-observation evidence only" in frontend
    assert "not connector health, reachability, operational freshness or current upstream availability claims" in frontend
    assert "does not prove live connectivity" in frontend
    assert "does not grant review authority, sharing approval or publication authority" in frontend
    assert "No attributable values are synthesized" in frontend
