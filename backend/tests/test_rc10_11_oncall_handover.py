from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs/operations/ON_CALL_HANDOVER.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_on_call_handover_contract_exists() -> None:
    assert DOC.is_file()
    text = _text()
    for marker in (
        "Primary on-call responder",
        "Secondary on-call responder",
        "Incident Commander",
        "Security lead",
        "Communications approver",
        "Severity escalation matrix",
        "Shift handover checklist",
        "Acceptance record required for human handover",
    ):
        assert marker in text


def test_handover_preserves_governance_and_separation_of_duties() -> None:
    text = _text()
    assert "Human share approval remains a separate human action" in text
    assert "do not gain publication approval" in text
    assert "Technical responders cannot self-approve publication" in text
    assert "does not change DTMO RBAC" in text


def test_handover_requires_real_human_acceptance_evidence() -> None:
    text = _text()
    for marker in (
        "named primary and secondary owners",
        "authoritative paging/contact paths are tested",
        "shift-handover checklist has been executed by real participants",
        "human exercise or supervised operational walkthrough",
        "service owner and operational owner sign off",
    ):
        assert marker in text


def test_handover_does_not_claim_staffing_or_acceptance() -> None:
    text = _text()
    assert "does **not** assign named production responders" in text
    assert "CI cannot prove that people are actually staffed, reachable, trained or approved" in text
    assert "must not claim that on-call coverage" in text


def test_handover_privacy_rules_exclude_sensitive_material() -> None:
    text = _text()
    assert "Do not copy credentials" in text
    assert "unnecessary personal data" in text
    assert "authentication tokens or secrets" in text
