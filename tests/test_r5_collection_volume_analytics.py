from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_collection_volume_is_aggregated_from_persisted_connector_runs():
    backend = read("backend/dtmo/command_center.py")
    assert '"collection_volume_distribution": []' in backend
    assert "select(ConnectorRun.connector_id, func.sum(ConnectorRun.inserted))" in backend
    assert ".group_by(ConnectorRun.connector_id)" in backend
    assert '"inserted": int(inserted or 0)' in backend


def test_visual_analytics_renders_collection_volume_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "collection_volume_distribution: CollectionVolumePoint[]" in frontend
    assert 'title="Collection volume"' in frontend
    assert 'labelKey="Connector"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_collection_volume_preserves_evidence_boundaries():
    backend = read("backend/dtmo/command_center.py")
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert 'data_state = "unavailable"' in backend
    assert "trends = _empty_trends()" in backend
    assert "historical execution evidence only" in frontend
    assert "does not prove live connectivity" in frontend
    assert "freshness" in frontend
    assert "connector health" in frontend
    assert "sharing approval or publication authority" in frontend
