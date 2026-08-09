from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github/workflows/phase8-staging-emulator-runtime.yml"
QA = ROOT / "docs/qa/PHASE8_STAGING_EMULATOR_RUNTIME_GATE.md"
PROBE = ROOT / "tools/phase8_staging_emulator_runtime_smoke.py"


def test_runtime_workflow_is_independently_observable_and_fail_closed() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Phase 8 Staging Emulator Runtime Gate" in text
    assert "phase8-staging-emulator-runtime-evidence" in text
    assert "staging-emulator-runtime-gate" in text
    assert 'test "$RESULT" = "success"' in text
    assert "github.event.pull_request.head.sha || github.sha" in text


def test_runtime_container_preserves_bounded_production_controls() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "DTMO_ENVIRONMENT=production" in text
    assert "DTMO_PUBLISH_REQUIRES_HUMAN_APPROVAL=true" in text
    assert "DTMO_FEATURE_LIVE_CONNECTORS=false" in text
    assert "--read-only" in text
    assert "--security-opt no-new-privileges:true" in text
    assert "--cap-drop ALL" in text
    assert "127.0.0.1:18000:8000" in text


def test_runtime_probe_checks_operational_and_security_behavior() -> None:
    text = PROBE.read_text(encoding="utf-8")
    for marker in (
        "/health",
        "/ready",
        "/connectors",
        "/connectors/cisa-kev/run",
        "/metrics",
        "human-approval-required",
        "api-key-and-rbac",
        "x-content-type-options",
        "x-frame-options",
        "referrer-policy",
        "x-correlation-id",
    ):
        assert marker in text


def test_runtime_qa_preserves_external_claim_boundary_and_governance() -> None:
    text = QA.read_text(encoding="utf-8")
    assert "CI_VALIDATION_PENDING" in text
    assert "human share approval" in text
    assert "does not prove a real staging environment" in text
    assert "does not satisfy the ten deployment-parity evidence classes" in text
    assert "does not complete Phase 8 or production acceptance" in text
