from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_phase8_2_prometheus_metrics_runbook_contract() -> None:
    runbook = (ROOT / "docs/qa/PHASE8_2_PROMETHEUS_METRICS_VALIDATION.md").read_text(encoding="utf-8")
    validator = (ROOT / "tools/phase8_platform_validation.py").read_text(encoding="utf-8")

    assert "Phase 8.2.11" in runbook
    assert "Prometheus" in runbook
    assert "healthy/up" in runbook
    assert "representative application request" in runbook
    assert "bearer tokens" in runbook
    assert "production monitoring credentials" in runbook
    assert "same immutable Phase 8.2 deployment fingerprint" in runbook
    assert "Repository CI" in runbook

    assert "prometheus_metrics" in validator
    assert "--check" in validator
