from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_investigation_handoff_status_uses_only_persisted_thehive_handoff_state():
    backend = read("backend/dtmo/command_center.py")
    assert "from dtmo.persistence.thehive import TheHiveHandoffState" in backend
    assert "select(TheHiveHandoffState.status, func.count())" in backend
    assert ".group_by(TheHiveHandoffState.status)" in backend
    assert '"investigation_handoff_status_distribution"' in backend


def test_visual_analytics_renders_investigation_handoff_status_with_accessible_table():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "investigation_handoff_status_distribution" in frontend
    assert 'title="Investigation handoff status"' in frontend
    assert 'labelKey="Persisted TheHive handoff status"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_investigation_handoff_status_preserves_evidence_and_authority_boundaries():
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    backend = read("backend/dtmo/command_center.py")
    assert "durable governed TheHive handoff records" in frontend
    assert "does not infer upstream case completeness" in frontend
    assert "local compromise, external-share authority or publication authority" in frontend
    assert "no attributable values are synthesized" in frontend.lower()
    assert "historical evidence only" in backend
    assert "proof of upstream case state" in backend
