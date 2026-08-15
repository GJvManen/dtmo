from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = (
    "environment_id",
    "accountable_owner",
    "deployed_release",
    "deployed_commit",
    "application_image_digest",
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
)

REQUIRED_PREREQUISITES = (
    "phase8_2_external_accepted",
    "phase8_3_external_accepted",
    "phase8_4_external_accepted",
    "same_immutable_identity_confirmed",
    "no_release_blocking_findings",
)

PLACEHOLDERS = {"", "pending", "todo", "tbd", "unknown", "n/a", "na"}


def _missing(value: Any) -> bool:
    return not isinstance(value, str) or value.strip().lower() in PLACEHOLDERS


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for field in REQUIRED_FIELDS:
        if _missing(payload.get(field)):
            errors.append(f"missing required field: {field}")

    commit = payload.get("deployed_commit", "")
    if isinstance(commit, str) and commit and not re.fullmatch(r"[0-9a-f]{40}", commit):
        errors.append("deployed_commit must be a 40-character lowercase git SHA")

    digest = payload.get("application_image_digest", "")
    if isinstance(digest, str) and digest and not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        errors.append("application_image_digest must be an immutable sha256 digest")

    prerequisites = payload.get("prerequisites")
    if not isinstance(prerequisites, dict):
        errors.append("prerequisites must be an object")
        prerequisites = {}
    if tuple(prerequisites.keys()) != REQUIRED_PREREQUISITES:
        errors.append("prerequisites must exactly match the required Phase 8.5 prerequisite order")
    for name in REQUIRED_PREREQUISITES:
        if prerequisites.get(name) is not True:
            errors.append(f"prerequisite not accepted: {name}")

    if payload.get("production_credentials_reused") is not False:
        errors.append("production_credentials_reused must be false")
    if payload.get("unsanitized_production_data_used") is not False:
        errors.append("unsanitized_production_data_used must be false")

    decision = payload.get("decision")
    if decision != "PASS / OWNER_ACCEPTED":
        errors.append("decision must be PASS / OWNER_ACCEPTED")
    if payload.get("phase8_5_pass") is not True:
        errors.append("phase8_5_pass must be true for acceptance")
    if payload.get("phase8_pass") is not True:
        errors.append("phase8_pass must be true only with accepted Phase 8.5 decision")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: phase8_5_accountable_staging_acceptance.py <manifest.json>", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: Phase 8.5 accountable staging acceptance is complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
