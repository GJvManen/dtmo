from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "ExposureWorkspace.tsx"


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


def test_exposure_preserves_provenance_and_no_exposure_inference() -> None:
    text = source()
    assert "Open evidence source" in text
    assert "raw evidence bound" in text
    assert "Prioritize vulnerabilities without inventing local exposure" in text
    assert "Neither the inventory nor its filters establish that a local asset is affected" in text
    assert "grant no scanner, remediation, case, publication or sharing authority" in text
