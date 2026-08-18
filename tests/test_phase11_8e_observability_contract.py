from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_observability_defaults_are_opt_in_and_structured():
    values = read("deploy/helm/dtmo/values.yaml")
    assert "observability:" in values
    assert "metrics:\n    enabled: false" in values
    assert "serviceMonitor:\n      enabled: false" in values
    assert "tracing:\n    enabled: false" in values
    assert "format: json" in values


def test_service_monitor_fails_closed_without_metrics():
    template = read("deploy/helm/dtmo/templates/observability.yaml")
    assert "ServiceMonitor" in template
    assert "observability.metrics.enabled must be true" in template
    assert "monitoring.coreos.com/v1" in template


def test_professional_observability_boundaries_are_documented():
    architecture = read("docs/architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md").lower()
    runbook = read("docs/operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md").lower()
    qa = read("docs/qa/PHASE11_8E_OBSERVABILITY_GATE.md").lower()
    for marker in ("metrics", "logs", "traces", "fail closed", "does not prove"):
        assert marker in architecture or marker in qa
    assert "rollback" in runbook
    assert "production authorization" in architecture
