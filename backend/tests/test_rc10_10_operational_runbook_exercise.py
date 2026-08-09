from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXERCISE = ROOT / "docs/operations/exercises/RUNBOOK_EXERCISE_20260809.md"


def _text() -> str:
    return EXERCISE.read_text(encoding="utf-8")


def test_controlled_exercise_document_exists_and_declares_boundary() -> None:
    assert EXERCISE.is_file()
    text = _text()
    for marker in (
        "controlled synthetic technical exercise",
        "no production data",
        "Human share approval remains mandatory",
        "not a substitute for human on-call handover",
    ):
        assert marker.lower() in text.lower()


def test_all_four_operational_scenarios_are_exercised() -> None:
    text = _text()
    for marker in (
        "Scenario 1 — API elevated 5xx",
        "Scenario 2 — connector/source degradation",
        "Scenario 3 — search-health red/unreachable",
        "Scenario 4 — storage-integrity alert",
        "dtmo_api_error_alert_active=1",
        "dtmo_connector_alert_active=1",
        "dtmo_search_health_alert_active=1",
        "dtmo_storage_integrity_alert_active=1",
    ):
        assert marker in text


def test_exercise_requires_evidence_containment_recovery_and_approval() -> None:
    text = _text().lower()
    for marker in (
        "preserve relevant logs",
        "reversible",
        "known-good",
        "objective validation",
        "human approval",
        "residual risk",
    ):
        assert marker in text


def test_exercise_preserves_governance_and_privacy() -> None:
    text = _text()
    for marker in (
        "RBAC unchanged",
        "separation of duties unchanged",
        "publication/share approval unchanged",
        "no production data or credentials used",
        "evidence/provenance preserved",
    ):
        assert marker in text


def test_exercise_records_residual_operational_gaps() -> None:
    text = _text()
    for marker in (
        "human on-call handover and operational ownership acceptance",
        "production contact/escalation roster approval",
        "human tabletop timing/decision-quality evidence",
        "external assurance gates in issue #1",
    ):
        assert marker in text
