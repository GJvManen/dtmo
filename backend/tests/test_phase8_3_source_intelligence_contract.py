from __future__ import annotations

import json
from pathlib import Path

from tools.phase8_3_source_intelligence_validation import REQUIRED_CHECKS, validate


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/qa/PHASE8_3_SOURCE_TO_INTELLIGENCE_VALIDATION.md"
TEMPLATE = ROOT / "docs/staging/PHASE8_3_SOURCE_INTELLIGENCE_EVIDENCE.template.json"


def test_phase8_3_runbook_is_fail_closed_and_identity_bound() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8.3" in text
    assert "same immutable post-E8 staging deployment" in text
    assert "source" in text
    assert "retrieval" in text
    assert "normalization" in text
    assert "deduplication" in text
    assert "PostgreSQL" in text
    assert "OpenSearch" in text
    assert "enrichment/correlation" in text
    assert "API" in text
    assert "canonical UI" in text
    assert "degraded" in text
    assert "Repository CI" in text
    assert "PASS / OWNER_ACCEPTED" in text


def test_phase8_3_template_and_validator_share_required_checks() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert tuple(payload["checks"].keys()) == REQUIRED_CHECKS
    assert payload["phase8_3_pass"] is False
    assert payload["phase8_pass"] is False
    errors = validate(payload)
    assert errors
    assert "missing required field: phase8_2_deployment_identity_fingerprint" in errors
    assert "check not PASS: approved_source" in errors


def test_phase8_3_validator_requires_complete_external_evidence() -> None:
    payload = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    for field in (
        "environment_id",
        "phase8_2_deployment_identity_fingerprint",
        "selected_source_id",
        "selected_source_type",
        "source_approval_reference",
        "retrieval_timestamp",
        "canonical_record_id",
        "audit_correlation_id",
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
            "evidence_reference": f"restricted://phase8-3/{name}",
        }
    payload["phase8_3_pass"] = True
    assert validate(payload) == []

    payload["phase8_pass"] = True
    assert "phase8_pass must remain false until Phase 8.4 and Phase 8.5 are accepted" in validate(payload)
