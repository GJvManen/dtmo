from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_phase8_2_privileged_administration_runbook_declares_external_boundary() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_PRIVILEGED_ADMINISTRATION_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    assert "Privileged Administration Controls Validation" in runbook
    assert "owner-approved" in runbook
    assert "same immutable Phase 8.2 deployment identity" in runbook
    assert "No production privileged credentials are reused" in runbook
    assert "Repository CI, browser fixtures, and synthetic authorization tests are supporting evidence only" in runbook


def test_phase8_2_privileged_administration_runbook_covers_positive_negative_and_audit_controls() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_PRIVILEGED_ADMINISTRATION_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    for requirement in (
        "non-privileged staging identity",
        "direct API access",
        "privileged staging identity",
        "destructive or sensitive action",
        "stale privilege persistence",
        "actor, action, target, outcome, timestamp, and correlation context",
        "client-supplied role/identity values",
    ):
        assert requirement in runbook


def test_phase8_2_privileged_administration_step_validator_is_documented_fail_closed() -> None:
    runbook = (ROOT / "docs/staging/PHASE8_2_PRIVILEGED_ADMINISTRATION_VALIDATION.md").read_text(
        encoding="utf-8"
    )
    validator = (ROOT / "tools/phase8_platform_validation.py").read_text(encoding="utf-8")
    assert "--check privileged_administration_controls" in runbook
    assert '"privileged_administration_controls"' in validator
    assert "phase8_2_pass` remains `false`" in runbook
    assert "phase8_pass` remains `false`" in runbook
