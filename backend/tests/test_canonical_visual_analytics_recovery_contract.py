from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "frontend/src/App.tsx"
WORKSPACE = ROOT / "frontend/src/VisualAnalyticsWorkspace.tsx"
AUDIT = ROOT / "docs/qa/PHASE11_10Q_FUNCTIONAL_COMPLETENESS_AUDIT.md"


def test_visual_analytics_is_a_canonical_workbench_surface():
    app = APP.read_text(encoding="utf-8")
    assert "./VisualAnalyticsWorkspace" in app
    assert "path: '/analytics'" in app
    assert "Visual Analytics" in app
    assert 'path="analytics"' in app
    assert "<VisualAnalyticsWorkspace" in app


def test_visual_analytics_uses_attributable_api_data_and_accessible_equivalents():
    text = WORKSPACE.read_text(encoding="utf-8")
    assert "/api/v1/command-center" in text
    assert "/api/v1/console/vulnerability-analytics" in text
    assert "aria-label" in text
    assert "<table" in text
    assert "No attributable" in text
    assert "synthetic" not in text.lower()


def test_visual_analytics_preserves_evidence_boundaries():
    text = WORKSPACE.read_text(encoding="utf-8")
    for marker in (
        "does not prove live connectivity",
        "does not prove local exposure",
        "does not grant review, sharing or publication authority",
    ):
        assert marker in text


def test_fq06_remains_the_bounded_recovery_driver_until_implementation_passes():
    audit = AUDIT.read_text(encoding="utf-8")
    assert "FQ-06 — Operator-grade charts/trends are absent from the canonical frontend" in audit
    assert "add an accessible visualization layer" in audit
    assert "no synthetic values may be used to make dashboards appear populated" in audit
