from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "ExposureWorkspace.tsx"
POPULATION = ROOT / "frontend" / "src" / "ThreatIntelligencePopulation.tsx"


def source() -> str:
    return WORKSPACE.read_text(encoding="utf-8")


def test_exposure_uses_canonical_same_origin_projection() -> None:
    text = source()
    assert "/api/v1/console/vulnerability-analytics?window=30d" in text
    assert "credentials: 'same-origin'" in text
    assert "Canonical DTMO API" in text
    assert "does not synthesize exposure state" in text


def test_exposure_supports_required_recovery_filters() -> None:
    text = source()
    for marker in (
        "Priority view",
        "CISA KEV evidence",
        "CVSS ≥ 9",
        "Vendor",
        "Product",
        "CWE",
        "Minimum EPSS (%)",
    ):
        assert marker in text
    assert "Missing attributes never satisfy a positive filter" in text
    assert "inventory.length > 0 && visible.length === 0" in text
    assert "Adjust the filters" in text


def test_exposure_empty_projection_exposes_governed_population_and_reload() -> None:
    text = source()
    population = POPULATION.read_text(encoding="utf-8")
    assert "inventory.length === 0" in text
    assert "<ThreatIntelligencePopulation" in text
    assert 'title="Populate canonical vulnerability evidence"' in text
    assert 'reloadLabel="Reload vulnerability evidence"' in text
    assert "void query.refetch()" in text
    assert "'/api/v1/admin/sources'" in population
    assert "/api/v1/admin/sources/${encodeURIComponent(sourceId)}/run" in population
    assert "method: 'POST'" in population
    assert "X-Request-ID" in population
    assert "Only already-enabled governed sources can be executed here" in population


def test_exposure_preserves_provenance_and_no_exposure_inference() -> None:
    text = source()
    population = POPULATION.read_text(encoding="utf-8")
    assert "Open evidence source" in text
    assert "raw evidence bound" in text
    assert "Prioritize vulnerabilities without inventing local exposure" in text
    assert "Neither population, the inventory nor its filters establish that a local asset is affected" in text
    assert "grant no scanner, remediation, case, publication or sharing authority" in text
    assert "Activation, endpoint changes and credentials stay in Sources & Collection" in population
    assert "does not approve intelligence for review, publication or external sharing" in population
