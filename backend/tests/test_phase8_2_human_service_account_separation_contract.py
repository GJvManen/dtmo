from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_phase8_2_human_service_account_separation_runbook_is_fail_closed() -> None:
    runbook = (
        ROOT / "docs/staging/PHASE8_2_HUMAN_SERVICE_ACCOUNT_SEPARATION_VALIDATION.md"
    ).read_text(encoding="utf-8")
    validator = (ROOT / "tools/phase8_platform_validation.py").read_text(encoding="utf-8")

    assert "human_service_account_separation" in validator
    assert "owner-approved post-E8 production-equivalent staging deployment" in runbook
    assert "same immutable Phase 8.2 deployment identity" in runbook
    assert "service account cannot perform interactive human login" in runbook
    assert "human accounts are not reused" in runbook
    assert "least-privilege" in runbook
    assert "separately managed and rotatable" in runbook
    assert "safe staging-only disable/revoke test" in runbook
    assert "audit records distinguish" in runbook
    assert "production human or service-account credentials are not reused" in runbook
    assert "phase8_2_pass: false" in runbook
    assert "phase8_pass: false" in runbook
    assert "--check human_service_account_separation" in runbook
    assert "must never be represented as external staging acceptance" in runbook
