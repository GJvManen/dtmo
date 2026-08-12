from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md"
PHASE8_GATE = ROOT / "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md"
RC13_GATE = ROOT / "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"


def test_prior_owner_acceptance_is_historical_and_rc13_is_reopened() -> None:
    text = RC13_GATE.read_text(encoding="utf-8")
    assert "Status: `REOPENED / BLOCKED_INTERNAL`" in text
    assert "2026-08-12" in text
    assert "RC13 owner retest akkoord" in text
    assert "subsequent project-owner functional retest" in text


def test_phase8_is_paused_while_external_identity_record_stays_fail_closed() -> None:
    text = PHASE8_GATE.read_text(encoding="utf-8")
    assert "PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST" in text
    assert "Issue #150" in text
    assert "Issue #158" in text
    assert "same immutable staging deployment identity" in text


def test_external_deployment_identity_record_fails_closed() -> None:
    text = RECORD.read_text(encoding="utf-8")
    for marker in (
        "decision: PENDING_EXTERNAL_DEPLOYMENT_IDENTITY",
        "evidence_complete: false",
        "phase8_pass: false",
        "environment_id: NOT_PROVIDED",
        "approved_endpoint: NOT_PROVIDED",
        "deployed_commit: NOT_PROVIDED",
        "application_image_digest: NOT_PROVIDED",
        "configuration_parity_record: NOT_PROVIDED",
        "external_validation_started: false",
        "project_owner_staging_acceptance: NOT_RECORDED",
    ):
        assert marker in text
    assert "secret value" in text.lower()
    assert "never grants intelligence publication" in text
