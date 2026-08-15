from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/qa/PHASE8_2_EVIDENCE_CONSOLIDATION_ACCEPTANCE.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"
TEMPLATE = ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json"


REQUIRED_CHECKS = (
    "application_health_readiness",
    "postgres_connectivity_migrations",
    "opensearch_health_search",
    "redis_coordination",
    "object_storage_read_write",
    "bearer_token_trust",
    "rbac_enforcement",
    "human_service_account_separation",
    "privileged_administration_controls",
    "audit_correlation",
    "prometheus_metrics",
    "grafana_dashboards",
)


def test_phase8_2_consolidation_runbook_is_fail_closed() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8.2.13" in text
    assert "same immutable Phase 8.2 deployment" in text
    assert "owner-approved" in text
    assert "phase8_2_pass" in text
    assert '"phase8_pass": false' in text
    assert "PASS / OWNER_ACCEPTED" in text
    assert "Fail closed" in text
    assert "Repository CI and synthetic fixtures are supporting evidence only" in text
    for check in REQUIRED_CHECKS:
        assert f"checks.{check}" in text


def test_complete_validator_and_template_share_all_phase8_2_checks() -> None:
    validator = VALIDATOR.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    for check in REQUIRED_CHECKS:
        assert check in validator
        assert f'"{check}"' in template
    assert "phase8_2_pass must be true only after all required checks have passed" in validator
    assert "phase8_pass must remain false until Phase 8.3-8.5 are accepted" in validator
