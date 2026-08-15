#!/usr/bin/env python3
"""Fail-closed validator for Phase 8.3 source-to-intelligence staging evidence."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "environment_id",
    "phase8_2_deployment_identity_fingerprint",
    "deployed_commit",
    "application_image_digest",
    "selected_source_id",
    "selected_source_type",
    "source_approval_reference",
    "retrieval_timestamp",
    "canonical_record_id",
    "audit_correlation_id",
    "evidence_location_reference",
    "validated_by",
    "validated_at",
)

REQUIRED_CHECKS = (
    "approved_source",
    "real_retrieval",
    "raw_evidence_provenance",
    "canonical_normalization",
    "deduplication_idempotency",
    "canonical_persistence_search",
    "enrichment_correlation",
    "vulnerability_cti_derivation",
    "api_ui_presentation",
    "governance_classification",
    "end_to_end_traceability",
    "degraded_upstream_behavior",
    "no_production_credentials",
)


def _load(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("evidence root must be an object")
    return payload


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip() or value == "NOT_PROVIDED":
            errors.append(f"missing required field: {field}")

    commit = payload.get("deployed_commit")
    if isinstance(commit, str) and commit != "NOT_PROVIDED" and (
        len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit)
    ):
        errors.append("deployed_commit must be a full lowercase 40-character Git SHA")

    digest = payload.get("application_image_digest")
    if isinstance(digest, str) and digest != "NOT_PROVIDED" and not (
        digest.startswith("sha256:") and len(digest) == 71
    ):
        errors.append("application_image_digest must be an immutable sha256 digest")

    checks = payload.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
    else:
        for name in REQUIRED_CHECKS:
            record = checks.get(name)
            if not isinstance(record, dict):
                errors.append(f"missing check record: {name}")
                continue
            if record.get("result") != "PASS":
                errors.append(f"check not PASS: {name}")
            evidence = record.get("evidence_reference")
            if not isinstance(evidence, str) or not evidence.strip() or evidence == "NOT_PROVIDED":
                errors.append(f"missing evidence reference: {name}")

    if payload.get("phase8_3_pass") is not True:
        errors.append("phase8_3_pass must be true only after all required checks have passed")
    if payload.get("phase8_pass") is True:
        errors.append("phase8_pass must remain false until Phase 8.4 and Phase 8.5 are accepted")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: phase8_3_source_intelligence_validation.py <manifest.json>")
        return 2
    payload = _load(Path(sys.argv[1]))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Phase 8.3 source-to-intelligence evidence: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
