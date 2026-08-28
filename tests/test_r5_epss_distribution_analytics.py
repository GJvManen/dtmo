from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_visual_analytics_buckets_canonical_epss_probabilities() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "epss?: number | null" in frontend
    assert "item.epss >= 0.75" in frontend
    assert "item.epss >= 0.5 && item.epss < 0.75" in frontend
    assert "item.epss >= 0.25 && item.epss < 0.5" in frontend
    assert "item.epss >= 0 && item.epss < 0.25" in frontend
    assert "typeof item.epss !== 'number'" in frontend
    assert 'title="EPSS probability distribution"' in frontend
    assert 'labelKey="EPSS probability band"' in frontend


def test_epss_distribution_preserves_evidence_and_authority_boundaries() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "passed the existing raw-evidence integrity boundary" in frontend
    assert "EPSS probabilities are prioritization evidence" in frontend
    assert "do not prove exploitability, local deployment or local exposure" in frontend
    assert "does not grant review authority, sharing approval or publication authority" in frontend
    assert "No attributable values are synthesized" in frontend


def test_vulnerability_pipeline_still_normalizes_epss_after_raw_integrity_verification() -> None:
    console = read("backend/dtmo/vulnerability_console.py")
    analytics = read("backend/dtmo/vulnerability_analytics.py")
    assert "actual_sha = sha256(payload).hexdigest()" in console
    assert "raw evidence integrity mismatch" in console
    assert '"epss": _float(vulnerability.get("epss"), minimum=0, maximum=1)' in analytics
