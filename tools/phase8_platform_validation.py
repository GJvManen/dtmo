#!/usr/bin/env python3
"""Validate Phase 8.2 platform/identity evidence against one immutable staging identity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

REQUIRED_CHECKS = (
    "application_health_readiness",
    "postgres_connectivity_migrations",
    "opensearch_health_search",
    "redis_coordination",
    "object_storage_read_write",
    "bearer_token_trust",
    "rbac_enforcement",
    "human_service_account_separation",
    "privileged_administration_controls",
    "audit_correlation",
    "prometheus_metrics",
    "grafana_separate_authentication",
)


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("evidence root must be an object")
    return value


def _fingerprint(payload: dict[str, Any]) -> str:
    identity = {
        "environment_id": payload.get("environment_id"),
        "deployed_commit": payload.get("deployed_commit"),
        "application_image_digest": payload.get("application_image_digest"),
        "supporting_image_digests": payload.get("supporting_image_digests"),
    }
    canonical = json.dumps(identity, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field in (
        "environment_id",
        "phase8_1_identity_fingerprint",
        "deployed_commit",
        "application_image_digest",
        "evidence_location_reference",
        "validated_by",
        "validated_at",
    ):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip() or value == "NOT_PROVIDED":
            errors.append(f"missing required field: {field}")

    commit = payload.get("deployed_commit")
    if isinstance(commit, str) and commit != "NOT_PROVIDED" and (len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit)):
        errors.append("deployed_commit must be a full lowercase 40-character Git SHA")

    digest = payload.get("application_image_digest")
    if isinstance(digest, str) and digest != "NOT_PROVIDED" and not (digest.startswith("sha256:") and len(digest) == 71):
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

    claimed = payload.get("deployment_identity_fingerprint")
    calculated = _fingerprint(payload)
    if claimed != calculated:
        errors.append("deployment_identity_fingerprint does not match the evidence identity fields")

    if payload.get("phase8_2_pass") is not True:
        errors.append("phase8_2_pass must be true only after all required checks have passed")
    if payload.get("phase8_pass") is True:
        errors.append("phase8_pass must remain false until Phase 8.3-8.5 are accepted")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--print-fingerprint", action="store_true")
    args = parser.parse_args()
    payload = _load(args.evidence)
    if args.print_fingerprint:
        print(_fingerprint(payload))
        return 0
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("Phase 8.2 platform and identity evidence: PASS")
    print(f"deployment_identity_fingerprint={_fingerprint(payload)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
