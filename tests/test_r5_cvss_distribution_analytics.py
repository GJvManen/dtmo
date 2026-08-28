from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_visual_analytics_buckets_canonical_cvss_scores() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "cvss?: number | null" in frontend
    assert "const vulnerabilityItems = vulnerability.data?.items ?? [];" in frontend
    assert "item.cvss >= 9" in frontend
    assert "item.cvss >= 7 && item.cvss < 9" in frontend
    assert "item.cvss >= 4 && item.cvss < 7" in frontend
    assert "item.cvss > 0 && item.cvss < 4" in frontend
    assert "item.cvss === 0" in frontend
    assert "typeof item.cvss !== 'number'" in frontend
    assert 'title="CVSS score distribution"' in frontend
    assert 'labelKey="CVSS score band"' in frontend


def test_cvss_distribution_preserves_evidence_and_authority_boundaries() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "passed the existing raw-evidence integrity boundary" in frontend
    assert "CVSS scores are prioritization evidence" in frontend
    assert "do not prove exploitability, local deployment or local exposure" in frontend
    assert "does not grant review authority, sharing approval or publication authority" in frontend
    assert "No attributable values are synthesized" in frontend


def test_vulnerability_pipeline_still_normalizes_cvss_after_raw_integrity_verification() -> None:
    console = read("backend/dtmo/vulnerability_console.py")
    analytics = read("backend/dtmo/vulnerability_analytics.py")
    assert "actual_sha = sha256(payload).hexdigest()" in console
    assert "raw evidence integrity mismatch" in console
    assert '"cvss": _max_cvss(vulnerability)' in analytics
