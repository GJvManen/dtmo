from __future__ import annotations

import json
from pathlib import Path

from tools.phase8_5_accountable_staging_acceptance import REQUIRED_PREREQUISITES, validate

ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/qa/PHASE8_5_ACCOUNTABLE_STAGING_ACCEPTANCE.md"
TEMPLATE = ROOT / "docs/staging/PHASE8_5_ACCOUNTABLE_STAGING_ACCEPTANCE.template.json"


def test_phase8_5_runbook_is_fail_closed_and_owner_bound() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    lower = text.lower()
    for term in (
        "accountable owner",
        "one immutable staging deployment identity",
        "phase 8.2",
        "phase 8.3",
        "phase 8.4",
        "release-blocking staging finding",
        "residual risks",
        "repository ci",
        "phase 9 independent external assurance",
    ):
        assert term in lower
    assert "PASS / OWNER_ACCEPTED" in text
    assert "BLOCKED" in text


def test_phase8_5_template_is_fail_closed() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert tuple(payload["prerequisites"].keys()) == REQUIRED_PREREQUISITES
    assert payload["decision"] == "BLOCKED"
    assert payload["phase8_5_pass"] is False
    assert payload["phase8_pass"] is False
    errors = validate(payload)
    assert "prerequisite not accepted: phase8_2_external_accepted" in errors
    assert "decision must be PASS / OWNER_ACCEPTED" in errors


def test_phase8_5_validator_requires_complete_owner_acceptance() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    for field in (
        "environment_id",
        "accountable_owner",
        "deployed_release",
        "supporting_images_runtime_fingerprint",
        "phase8_deployment_identity_fingerprint",
        "phase8_2_acceptance_reference",
        "phase8_3_acceptance_reference",
        "phase8_4_acceptance_reference",
        "approved_deviations_reference",
        "residual_risks_reference",
        "rollback_change_reference",
        "evidence_package_reference",
        "validated_by",
        "validated_at",
    ):
        payload[field] = "evidence-value"
    payload["deployed_commit"] = "a" * 40
    payload["application_image_digest"] = "sha256:" + "b" * 64
    for name in REQUIRED_PREREQUISITES:
        payload["prerequisites"][name] = True
    payload["decision"] = "PASS / OWNER_ACCEPTED"
    payload["phase8_5_pass"] = True
    payload["phase8_pass"] = True
    assert validate(payload) == []

    payload["prerequisites"]["same_immutable_identity_confirmed"] = False
    assert "prerequisite not accepted: same_immutable_identity_confirmed" in validate(payload)
