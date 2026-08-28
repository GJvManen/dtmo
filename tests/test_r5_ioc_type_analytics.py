from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_ioc_type_distribution_uses_persisted_canonical_observables() -> None:
    backend = read("backend/dtmo/command_center.py")
    assert '"ioc_type_distribution": []' in backend
    assert "select(IntelOwlEnrichmentRecord.observable_type, func.count())" in backend
    assert ".group_by(IntelOwlEnrichmentRecord.observable_type)" in backend
    assert '"observable_type": str(observable_type)' in backend


def test_visual_analytics_renders_accessible_ioc_type_distribution() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "ioc_type_distribution: IocTypePoint[]" in frontend
    assert 'title="IOC type distribution"' in frontend
    assert 'labelKey="Observable type"' in frontend
    assert 'aria-label={`${title} table`}' in frontend


def test_ioc_type_analytics_preserves_evidence_and_authority_boundaries() -> None:
    frontend = read("frontend/src/VisualAnalyticsWorkspace.tsx")
    assert "does not infer maliciousness or local compromise" in frontend
    assert "does not prove live connectivity" in frontend
    assert "does not prove local exposure" in frontend
    assert "sharing approval or publication authority" in frontend
