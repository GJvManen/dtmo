from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/qa/PHASE8_2_GRAFANA_DASHBOARDS_VALIDATION.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"


def test_phase8_2_grafana_runbook_exists_and_is_fail_closed() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8.2.12" in text
    assert "checks.grafana_dashboards" in text
    assert "--check grafana_dashboards" in text
    assert "owner-approved" in text
    assert "same immutable Phase 8.2 deployment" in text
    assert "production" in text
    assert "authentication loop" in text
    assert "authorization" in text
    assert "provisioning" in text
    assert "restart" in text
    assert "PASS" in text
    assert "Repository CI" in text


def test_phase8_platform_validator_supports_grafana_step_scope() -> None:
    source = VALIDATOR.read_text(encoding="utf-8")
    assert "grafana_dashboards" in source
    assert "--check" in source
    assert "checks" in source
