from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_phase8_2_bearer_token_trust_runbook_is_fail_closed_and_identity_bound() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_BEARER_TOKEN_TRUST_VALIDATION.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "owner-approved post-E8 production-equivalent staging deployment",
        "same immutable Phase 8.2 deployment identity",
        "valid staging bearer token",
        "without a token",
        "expired token",
        "invalid signature",
        "wrong issuer or audience",
        "verified token claims",
        "production credentials/signing material",
        "without logging bearer-token material or signing secrets",
        "checks.bearer_token_trust.result",
        "--check bearer_token_trust",
        "phase8_2_pass",
        "phase8_pass",
    ):
        assert required in runbook

    assert "Repository CI, unit tests and synthetic token fixtures are supporting evidence only" in runbook
    assert "Record `FAIL` rather than `PASS`" in runbook


def test_phase8_2_validator_exposes_bearer_token_trust_as_step_scoped_check() -> None:
    validator = (ROOT / "tools/phase8_platform_validation.py").read_text(encoding="utf-8")
    evidence_template = (
        ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json"
    ).read_text(encoding="utf-8")

    assert '"bearer_token_trust"' in validator
    assert '"bearer_token_trust"' in evidence_template
    assert "phase8_2_pass must remain false during step-scoped validation" in validator
    assert "phase8_pass must remain false during step-scoped validation" in validator
