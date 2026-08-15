from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / "docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md"
PHASE8_GATE = ROOT / "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md"
RC13_GATE = ROOT / "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"


def test_accountable_owner_acceptance_closes_rc13_without_claiming_external_acceptance() -> None:
    text = RC13_GATE.read_text(encoding="utf-8")
    assert "PASS / OWNER_ACCEPTED" in text
    assert "2026-08-12" in text
    assert "Accepted canonical journey" in text
    assert "Accountable owner acceptance" in text
    assert "historical evidence must remain immutable" in text
    assert "READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY" in text
    assert "CI/browser fixtures cannot create external staging or production acceptance" in text


def test_phase8_owner_approved_staging_still_requires_immutable_identity_binding() -> None:
    text = PHASE8_GATE.read_text(encoding="utf-8")
    assert "ACTIVE_EXTERNAL_VALIDATION / OWNER_APPROVED_STAGING / IMMUTABLE_EVIDENCE_BINDING_INCOMPLETE" in text
    assert "PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE" in text
    assert "APPROVED / OWNER_VERIFIED_EXTERNAL_EVIDENCE" in text
    assert "Issue #158" in text
    assert "one immutable deployment identity" in text
    assert "Phase 8 is complete only when the immutable staging identity is complete and approved" in text
    assert "Repository CI, local Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this gate by themselves" in text


def test_external_deployment_identity_record_fails_closed_until_binding_complete() -> None:
    text = RECORD.read_text(encoding="utf-8")
    for marker in (
        "decision: OWNER_VERIFIED_EXTERNAL_DEPLOYMENT_IDENTITY_BINDING_INCOMPLETE",
        "evidence_complete: false",
        "phase8_pass: false",
        "external_deployment_owner_test: PASS_OWNER_VERIFIED",
        "staging_environment_approval: PASS_OWNER_VERIFIED",
        "environment_id: NOT_PROVIDED",
        "approved_endpoint: NOT_PROVIDED",
        "deployed_commit: NOT_PROVIDED",
        "application_image_digest: NOT_PROVIDED",
        "configuration_parity_record: NOT_PROVIDED",
        "external_validation_started: true",
        "phase8_2_status: IN_PROGRESS",
        "phase8_5_accountable_acceptance: NOT_RECORDED",
    ):
        assert marker in text
    assert "secret value" in text.lower()
    assert "never grants intelligence publication" in text
