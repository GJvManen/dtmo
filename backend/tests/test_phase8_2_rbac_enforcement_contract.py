from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_phase8_2_rbac_runbook_preserves_external_evidence_boundary() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_RBAC_ENFORCEMENT_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    assert "REPOSITORY_CONTRACT_READY / EXTERNAL_EVIDENCE_REQUIRED" in runbook
    assert "owner-approved post-E8 production-equivalent staging deployment" in runbook
    assert "same immutable Phase 8.2 deployment identity" in runbook
    assert "Production IAM credentials" in runbook
    assert "supporting evidence only" in runbook


def test_phase8_2_rbac_runbook_requires_positive_and_negative_authorization() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_RBAC_ENFORCEMENT_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    assert "least-privilege" in runbook
    assert "fail-closed denial" in runbook
    assert "privileged identity" in runbook
    assert "direct API requests enforce the same authorization boundary as the UI" in runbook
    assert "client-controlled role/identity headers" in runbook
    assert "stale privileges are not retained" in runbook
    assert "observable/auditable evidence" in runbook


def test_phase8_2_rbac_runbook_uses_step_scoped_validator() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_RBAC_ENFORCEMENT_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    validator = (ROOT / "tools/phase8_platform_validation.py").read_text(encoding="utf-8")
    assert '"rbac_enforcement"' in validator
    assert "checks.rbac_enforcement" in runbook
    assert "--check rbac_enforcement" in runbook
    assert "`phase8_2_pass` and `phase8_pass` must remain `false`" in runbook
