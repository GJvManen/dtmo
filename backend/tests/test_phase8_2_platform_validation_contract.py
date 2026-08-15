from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Any, cast


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json"
WORKFLOW = ROOT / ".github/workflows/phase8-platform-identity-validation.yml"
RUNBOOK = ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_VALIDATION.md"
STEP_RUNBOOK = ROOT / "docs/staging/PHASE8_2_STEP_SCOPED_VALIDATION.md"
VALIDATOR_PATH = ROOT / "tools/phase8_platform_validation.py"


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("phase8_platform_validation", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_VALIDATOR = _load_validator()
REQUIRED_CHECKS = cast(tuple[str, ...], _VALIDATOR.REQUIRED_CHECKS)
validate = cast(Any, _VALIDATOR.validate)
validate_check = cast(Any, _VALIDATOR.validate_check)


def _valid_payload() -> dict[str, object]:
    payload: dict[str, object] = {
        "environment_id": "staging-approved-01",
        "phase8_1_identity_fingerprint": "a" * 64,
        "deployed_commit": "b" * 40,
        "application_image_digest": "sha256:" + "c" * 64,
        "supporting_image_digests": {"postgres": "sha256:" + "d" * 64},
        "evidence_location_reference": "restricted-evidence://phase8/staging-approved-01",
        "validated_by": "accountable-staging-owner",
        "validated_at": "2026-08-14T11:00:00Z",
        "checks": {
            name: {"result": "PASS", "evidence_reference": f"restricted-evidence://phase8/{name}"}
            for name in REQUIRED_CHECKS
        },
        "phase8_2_pass": True,
        "phase8_pass": False,
    }
    identity = {
        "environment_id": payload["environment_id"],
        "deployed_commit": payload["deployed_commit"],
        "application_image_digest": payload["application_image_digest"],
        "supporting_image_digests": payload["supporting_image_digests"],
    }
    canonical = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    payload["deployment_identity_fingerprint"] = hashlib.sha256(canonical).hexdigest()
    return payload


def _step_payload(check_name: str) -> dict[str, object]:
    payload = _valid_payload()
    payload["phase8_2_pass"] = False
    checks = cast(dict[str, dict[str, str]], payload["checks"])
    for name in REQUIRED_CHECKS:
        if name != check_name:
            checks[name] = {"result": "NOT_RUN", "evidence_reference": "NOT_PROVIDED"}
    return payload


def test_template_is_fail_closed() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    errors = validate(payload)
    assert errors
    assert payload["phase8_2_pass"] is False
    assert payload["phase8_pass"] is False


def test_complete_phase8_2_payload_passes_without_completing_phase8() -> None:
    payload = _valid_payload()
    assert validate(payload) == []
    assert payload["phase8_pass"] is False


def test_missing_required_platform_check_fails() -> None:
    payload = _valid_payload()
    del payload["checks"]["audit_correlation"]  # type: ignore[index]
    errors = validate(payload)
    assert "missing check record: audit_correlation" in errors


def test_phase8_cannot_be_claimed_complete_from_phase8_2() -> None:
    payload = _valid_payload()
    payload["phase8_pass"] = True
    assert "phase8_pass must remain false until Phase 8.3-8.5 are accepted" in validate(payload)


def test_step_scoped_health_validation_passes_with_future_checks_not_run() -> None:
    payload = _step_payload("application_health_readiness")
    assert validate_check(payload, "application_health_readiness") == []
    assert validate(payload)


def test_step_scoped_postgres_validation_passes_with_future_checks_not_run() -> None:
    payload = _step_payload("postgres_connectivity_migrations")
    assert validate_check(payload, "postgres_connectivity_migrations") == []


def test_step_scoped_validation_requires_identity_and_evidence_reference() -> None:
    payload = _step_payload("postgres_connectivity_migrations")
    payload["deployed_commit"] = "NOT_PROVIDED"
    checks = cast(dict[str, dict[str, str]], payload["checks"])
    checks["postgres_connectivity_migrations"]["evidence_reference"] = "NOT_PROVIDED"
    errors = validate_check(payload, "postgres_connectivity_migrations")
    assert "missing required field: deployed_commit" in errors
    assert "missing evidence reference: postgres_connectivity_migrations" in errors


def test_step_scoped_validation_cannot_claim_phase8_2_pass() -> None:
    payload = _step_payload("application_health_readiness")
    payload["phase8_2_pass"] = True
    assert "phase8_2_pass must remain false during step-scoped validation" in validate_check(
        payload, "application_health_readiness"
    )


def test_workflow_and_runbook_bind_to_same_identity() -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")
    step_runbook = STEP_RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8 Platform Identity Validation Gate" in workflow
    assert "test_phase8_2_platform_validation_contract.py" in workflow
    assert "same immutable staging deployment identity" in runbook
    assert "--check postgres_connectivity_migrations" in step_runbook
    assert "Phase 8.3" in runbook
