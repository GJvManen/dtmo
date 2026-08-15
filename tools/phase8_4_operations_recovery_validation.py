from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED_CHECKS = (
    "service_recovery",
    "postgres_backup_restore",
    "object_storage_recovery",
    "opensearch_recovery",
    "cache_queue_recovery",
    "application_rollback",
    "migration_recovery",
    "iam_secrets_continuity",
    "observability_continuity",
    "degraded_dependencies",
    "rto_rpo_observations",
    "change_rollback_evidence",
)

REQUIRED_FIELDS = (
    "environment_id",
    "phase8_2_deployment_identity_fingerprint",
    "phase8_3_evidence_fingerprint",
    "deployed_commit",
    "application_image_digest",
    "recovery_window_reference",
    "evidence_location_reference",
    "validated_by",
    "validated_at",
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

    checks = payload.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
        checks = {}
    if tuple(checks.keys()) != REQUIRED_CHECKS:
        errors.append("checks must exactly match the required Phase 8.4 check order")
    for name in REQUIRED_CHECKS:
        item = checks.get(name, {})
        if not isinstance(item, dict) or item.get("result") != "PASS":
            errors.append(f"check not PASS: {name}")
        if not isinstance(item, dict) or _missing(item.get("evidence_reference")):
            errors.append(f"missing evidence reference: {name}")

    if payload.get("production_credentials_reused") is not False:
        errors.append("production_credentials_reused must be false")
    if payload.get("unsanitized_production_data_used") is not False:
        errors.append("unsanitized_production_data_used must be false")
    if payload.get("phase8_4_pass") is not True:
        errors.append("phase8_4_pass must be true for acceptance")
    if payload.get("phase8_pass") is not False:
        errors.append("phase8_pass must remain false until Phase 8.5 is accepted")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: phase8_4_operations_recovery_validation.py <manifest.json>", file=sys.stderr)
        return 2
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: Phase 8.4 operations/recovery evidence is complete and fail-closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
