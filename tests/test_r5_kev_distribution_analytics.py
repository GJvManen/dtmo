from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_visual_analytics_uses_canonical_vulnerability_rows_for_kev_distribution() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "type VulnerabilityItem = { kev?: boolean | null };" in frontend
    assert "const vulnerabilityItems = vulnerability.data?.items ?? [];" in frontend
    assert "item.kev === true" in frontend
    assert "item.kev === false" in frontend
    assert "item.kev !== true && item.kev !== false" in frontend
    assert 'title="KEV status distribution"' in frontend
    assert 'labelKey="KEV evidence status"' in frontend


def test_kev_distribution_preserves_evidence_and_authority_boundaries() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "passed the existing raw-evidence integrity boundary" in frontend
    assert "does not prove local deployment, exploitability or compromise" in frontend
    assert "does not grant review authority, sharing approval or publication authority" in frontend
    assert "No attributable values are synthesized" in frontend


def test_vulnerability_pipeline_still_verifies_raw_evidence_before_projection() -> None:
    console = read("backend/dtmo/vulnerability_console.py")
    assert "actual_sha = sha256(payload).hexdigest()" in console
    assert "raw evidence integrity mismatch" in console
    assert "project_vulnerability_analytics(" in console
