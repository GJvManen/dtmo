from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_collection_observation_age_uses_latest_persisted_run_start():
    backend = read("backend/dtmo/command_center.py")
    assert '"collection_observation_age": []' in backend
    assert "func.max(ConnectorRun.started_at)" in backend
    assert '"last_started_at": _as_utc(last_started_at).isoformat()' in backend
    assert '"age_hours": round(' in backend


def test_visual_analytics_renders_collection_observation_age_accessibly():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "collection_observation_age: CollectionObservationAgePoint[]" in frontend
    assert 'title="Collection observation age"' in frontend
    assert 'valueKey="Hours since latest persisted run start"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_collection_observation_age_preserves_evidence_boundaries():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "historical observation evidence only" in frontend
    assert "does not prove live connectivity" in frontend
    assert "does not prove local exposure" in frontend
    assert "does not prove source reachability" in frontend
    assert "connector health, operational freshness or current upstream availability" in frontend
    assert "sharing approval or publication authority" in frontend
