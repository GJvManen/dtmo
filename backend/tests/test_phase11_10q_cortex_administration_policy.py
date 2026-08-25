from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend/src/AdministrationWorkspace.tsx"
BACKEND = ROOT / "backend/dtmo/admin_center.py"
READINESS = ROOT / "backend/dtmo/integration_readiness.py"
ANALYSIS = ROOT / "frontend/src/AnalysisWorkspace.tsx"


def test_cortex_analyzer_policy_is_configurable_from_canonical_administration() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    backend = BACKEND.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")

    assert "Cortex analyzer allowlist" in workspace
    assert "cortex_allowed_analyzers" in workspace
    assert "cortex_allowed_analyzers" in backend
    assert 'integration_id in {"ail", "intelowl", "cortex"}' in backend
    assert "Cortex analyzer allowlist is only valid for the Cortex integration" in backend
    assert 'integration_id == "cortex" and not settings.cortex_allowed_analyzers.strip()' in readiness


def test_cortex_policy_uses_shared_fail_closed_readiness() -> None:
    backend = BACKEND.read_text(encoding="utf-8")
    assert "integration_readiness(settings)" in backend
    assert '"cortex_allowed_analyzers": settings.cortex_allowed_analyzers if integration_id == "cortex" else ""' in backend
    assert 'values["cortex_allowed_analyzers"] = settings.cortex_allowed_analyzers' in backend


def test_cortex_execution_remains_in_governed_analysis_workspace() -> None:
    workspace = WORKSPACE.read_text(encoding="utf-8")
    analysis = ANALYSIS.read_text(encoding="utf-8")
    assert "Cortex execution itself remains in the governed Analysis &amp; Enrichment workflow" in workspace
    assert "Run Cortex" in analysis
    assert "Run Cortex" not in workspace
