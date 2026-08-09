from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNBOOK_DIR = ROOT / "docs/operations/runbooks"
RUNBOOKS = {
    "index": RUNBOOK_DIR / "README.md",
    "api": RUNBOOK_DIR / "API_OUTAGE.md",
    "connector": RUNBOOK_DIR / "CONNECTOR_FAILURE.md",
    "search": RUNBOOK_DIR / "SEARCH_HEALTH_DEGRADATION.md",
    "storage": RUNBOOK_DIR / "STORAGE_INTEGRITY_RECOVERY.md",
}


def _text(name: str) -> str:
    return RUNBOOKS[name].read_text(encoding="utf-8")


def test_runbook_set_exists_and_has_common_response_controls() -> None:
    for path in RUNBOOKS.values():
        assert path.is_file()
    index = _text("index")
    for marker in (
        "Incident Commander",
        "SEV-1",
        "Evidence and privacy rules",
        "Contain safely",
        "Recover from a known-good state",
        "human share approval",
        "Exercise boundary",
    ):
        assert marker in index


def test_service_runbooks_have_trigger_containment_recovery_communication_and_closure() -> None:
    for name in ("api", "connector", "search", "storage"):
        text = _text(name)
        for section in (
            "## Trigger",
            "## Immediate checks",
            "## Containment",
            "## Recovery",
            "## Security / privacy branch",
            "## Communication",
            "## Closure criteria",
        ):
            assert section in text


def test_runbooks_bind_to_existing_bounded_alert_metrics() -> None:
    assert "dtmo_api_error_alert_active" in _text("api")
    assert "dtmo_connector_alert_active" in _text("connector")
    assert "dtmo_search_health_alert_active" in _text("search")
    assert "dtmo_storage_integrity_alert_active" in _text("storage")


def test_runbooks_preserve_governance_and_publication_separation() -> None:
    joined = "\n".join(path.read_text(encoding="utf-8") for path in RUNBOOKS.values())
    assert "Human review/share approval remains mandatory" in joined or "human share approval remains mandatory" in joined
    assert "Do not disable RBAC" in joined
    assert "connectors never gain share approval" in joined
    assert "External or broad internal communication requires" in joined


def test_runbooks_require_evidence_preservation_and_known_good_recovery() -> None:
    index = _text("index")
    storage = _text("storage")
    assert "Preserve relevant logs and immutable/raw evidence" in index
    assert "known-good" in index.lower()
    assert "known-good immutable source/backup" in storage
    assert "integrity and provenance checks" in storage


def test_runbooks_do_not_claim_exercise_or_phase_completion() -> None:
    index = _text("index")
    assert "not considered exercised" in index
    assert "Phase 7 still requires" in index
