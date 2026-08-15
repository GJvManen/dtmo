from __future__ import annotations

import json
from pathlib import Path

from tools.phase8_4_operations_recovery_validation import REQUIRED_CHECKS, validate

ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/qa/PHASE8_4_OPERATIONS_RECOVERY_VALIDATION.md"
TEMPLATE = ROOT / "docs/staging/PHASE8_4_OPERATIONS_RECOVERY_EVIDENCE.template.json"


def test_phase8_4_runbook_is_external_fail_closed_and_identity_bound() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    lower = text.lower()
    for term in (
        "same immutable post-e8 production-equivalent staging deployment",
        "service recovery",
        "backup/restore",
        "application rollback",
        "migration recovery",
        "iam/secrets continuity",
        "observability continuity",
        "degraded dependencies",
        "rto/rpo",
        "repository ci",
    ):
        assert term in lower
    assert "PASS / OWNER_ACCEPTED" in text


def test_phase8_4_template_and_validator_share_required_checks() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert tuple(payload["checks"].keys()) == REQUIRED_CHECKS
    assert payload["phase8_4_pass"] is False
    assert payload["phase8_pass"] is False
    errors = validate(payload)
    assert errors
    assert "missing required field: phase8_2_deployment_identity_fingerprint" in errors
    assert "check not PASS: service_recovery" in errors


def test_phase8_4_validator_requires_complete_external_evidence() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    for field in (
        "environment_id",
        "phase8_2_deployment_identity_fingerprint",
        "phase8_3_evidence_fingerprint",
        "recovery_window_reference",
        "evidence_location_reference",
        "validated_by",
        "validated_at",
    ):
        payload[field] = "evidence-value"
    payload["deployed_commit"] = "a" * 40
    payload["application_image_digest"] = "sha256:" + "b" * 64
    for name in REQUIRED_CHECKS:
        payload["checks"][name] = {
            "result": "PASS",
            "evidence_reference": f"restricted://phase8-4/{name}",
        }
    payload["phase8_4_pass"] = True
    assert validate(payload) == []

    payload["phase8_pass"] = True
    assert "phase8_pass must remain false until Phase 8.5 is accepted" in validate(payload)
