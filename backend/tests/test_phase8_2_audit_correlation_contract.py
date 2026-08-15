from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/staging/PHASE8_2_AUDIT_CORRELATION_VALIDATION.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"


def test_audit_correlation_runbook_binds_external_evidence_to_immutable_staging_identity() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8.2.10" in text
    assert "owner-approved production-equivalent staging deployment" in text
    assert "same immutable Phase 8.2 deployment fingerprint" in text
    assert "production credentials" in text
    assert "Repository CI and synthetic fixtures are supporting evidence only" in text


def test_audit_correlation_runbook_requires_attribution_correlation_and_secret_hygiene() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    for phrase in (
        "actor, action, target, outcome, timestamp, and correlation context",
        "trace it through the relevant application and audit records",
        "human and service-account actor identities are distinguishable",
        "bearer tokens",
        "Event timestamps permit reconstruction of event order",
        "Audit visibility follows the intended authorization boundary",
    ):
        assert phrase in text


def test_step_scoped_validator_supports_audit_correlation_without_claiming_phase8_complete() -> None:
    source = VALIDATOR.read_text(encoding="utf-8")
    assert '"audit_correlation"' in source
    assert "--check" in source
    assert "phase8_2_pass must remain false during step-scoped validation" in source
    assert "phase8_pass must remain false during step-scoped validation" in source
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "--check audit_correlation" in text
    assert "phase8_2_pass" in text
    assert "phase8_pass" in text
