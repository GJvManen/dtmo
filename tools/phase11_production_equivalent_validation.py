from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_EVIDENCE_CLASSES = (
    "immutable_candidate_identity",
    "migration_compatibility",
    "upgrade",
    "rollback",
    "health",
    "saturation",
    "recovery",
)

PLACEHOLDER_VALUES = {
    "",
    "required",
    "pending",
    "todo",
    "tbd",
    "n/a",
    "na",
    "none",
    "null",
    "placeholder",
}

HISTORICAL_ONLY_MARKERS = (
    "phase8",
    "phase 8",
    "phase9",
    "phase 9",
    "historical candidate",
)

SYNTHETIC_ONLY_MARKERS = (
    "synthetic fixture",
    "staging emulator",
    "repository ci",
    "github actions only",
    "localhost",
)

SHA40_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
FINGERPRINT_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def build_contract() -> dict[str, object]:
    return {
        "phase": "11.10",
        "status": "IN_PROGRESS",
        "candidate_identity_policy": "single immutable integrated deployment identity",
        "required_evidence_classes": list(REQUIRED_EVIDENCE_CLASSES),
        "historical_phase8_evidence_reusable": False,
        "fresh_candidate_bound_evidence_required": True,
        "same_candidate_required_for_phase11_11": True,
        "missing_or_ambiguous_evidence": "FAIL_CLOSED",
        "final_manifest_decision": "PASS / OWNER_ACCEPTED",
        "production_authorized": False,
    }


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _is_placeholder(value: Any) -> bool:
    text = _text(value)
    if not text:
        return True
    lowered = text.lower()
    if lowered in PLACEHOLDER_VALUES:
        return True
    return "required" in lowered or "placeholder" in lowered


def _is_iso_timestamp(value: Any) -> bool:
    text = _text(value)
    if _is_placeholder(text):
        return False
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def _as_mapping(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def candidate_identity_material(manifest: dict[str, Any]) -> dict[str, object]:
    environment = _as_mapping(manifest.get("environment"))
    candidate = _as_mapping(manifest.get("candidate"))
    supporting = sorted(_text(item) for item in _as_list(candidate.get("supporting_image_digests")))
    return {
        "environment_id": _text(environment.get("environment_id")),
        "deployed_commit": _text(candidate.get("deployed_commit")),
        "application_image_digest": _text(candidate.get("application_image_digest")),
        "supporting_image_digests": supporting,
        "migration_head": _text(candidate.get("migration_head")),
        "deployment_revision": _text(candidate.get("deployment_revision")),
    }


def calculate_candidate_fingerprint(manifest: dict[str, Any]) -> str:
    material = candidate_identity_material(manifest)
    canonical = json.dumps(material, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def _validate_identity(manifest: dict[str, Any], errors: list[str]) -> str:
    environment = _as_mapping(manifest.get("environment"))
    candidate = _as_mapping(manifest.get("candidate"))

    if _text(manifest.get("phase")) != "11.10":
        errors.append("phase must be 11.10")
    if _text(manifest.get("schema_version")) != "1.0":
        errors.append("schema_version must be 1.0")
    if _text(environment.get("environment_class")) != "production-equivalent":
        errors.append("environment_class must be production-equivalent")

    for field in (
        "environment_id",
        "accountable_owner",
        "validation_operator",
        "security_release_reviewer",
    ):
        if _is_placeholder(environment.get(field)):
            errors.append(f"environment.{field} must be populated")

    deployed_commit = _text(candidate.get("deployed_commit"))
    if not SHA40_RE.fullmatch(deployed_commit) or deployed_commit == "0" * 40:
        errors.append("candidate.deployed_commit must be a non-zero 40-character lowercase Git SHA")

    application_digest = _text(candidate.get("application_image_digest"))
    if not DIGEST_RE.fullmatch(application_digest):
        errors.append("candidate.application_image_digest must be an immutable sha256 digest")

    prior_digest = _text(candidate.get("prior_application_image_digest"))
    if not DIGEST_RE.fullmatch(prior_digest):
        errors.append("candidate.prior_application_image_digest must be an immutable sha256 digest")
    elif prior_digest == application_digest:
        errors.append("candidate.prior_application_image_digest must differ from the candidate digest")

    for digest in _as_list(candidate.get("supporting_image_digests")):
        if not DIGEST_RE.fullmatch(_text(digest)):
            errors.append("every candidate.supporting_image_digests entry must be an immutable sha256 digest")

    for field in ("migration_head", "deployment_revision"):
        if _is_placeholder(candidate.get(field)):
            errors.append(f"candidate.{field} must be populated")

    expected = calculate_candidate_fingerprint(manifest)
    supplied = _text(candidate.get("candidate_fingerprint"))
    if not FINGERPRINT_RE.fullmatch(supplied):
        errors.append("candidate.candidate_fingerprint must be a sha256 fingerprint")
    elif supplied != expected:
        errors.append("candidate.candidate_fingerprint does not match immutable candidate identity material")

    validation_window = _as_mapping(manifest.get("validation_window"))
    started = validation_window.get("started_at")
    completed = validation_window.get("completed_at")
    if not _is_iso_timestamp(started):
        errors.append("validation_window.started_at must be an offset-aware ISO-8601 timestamp")
    if not _is_iso_timestamp(completed):
        errors.append("validation_window.completed_at must be an offset-aware ISO-8601 timestamp")
    if _is_iso_timestamp(started) and _is_iso_timestamp(completed):
        start_dt = datetime.fromisoformat(_text(started).replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(_text(completed).replace("Z", "+00:00"))
        if end_dt < start_dt:
            errors.append("validation_window.completed_at must not precede started_at")

    return expected


def _reference_is_acceptable(value: Any) -> bool:
    text = _text(value)
    if _is_placeholder(text):
        return False
    lowered = text.lower()
    if any(marker in lowered for marker in HISTORICAL_ONLY_MARKERS):
        return False
    if any(marker in lowered for marker in SYNTHETIC_ONLY_MARKERS):
        return False
    return True


def _validate_evidence(manifest: dict[str, Any], expected_fingerprint: str, errors: list[str]) -> None:
    evidence = _as_mapping(manifest.get("evidence"))
    candidate = _as_mapping(manifest.get("candidate"))
    environment = _as_mapping(manifest.get("environment"))

    if set(evidence) != set(REQUIRED_EVIDENCE_CLASSES):
        missing = sorted(set(REQUIRED_EVIDENCE_CLASSES) - set(evidence))
        unexpected = sorted(set(evidence) - set(REQUIRED_EVIDENCE_CLASSES))
        if missing:
            errors.append("missing evidence classes: " + ", ".join(missing))
        if unexpected:
            errors.append("unexpected evidence classes: " + ", ".join(unexpected))

    for evidence_class in REQUIRED_EVIDENCE_CLASSES:
        item = _as_mapping(evidence.get(evidence_class))
        prefix = f"evidence.{evidence_class}"
        if _text(item.get("status")) != "PASS":
            errors.append(f"{prefix}.status must be PASS")
        if _text(item.get("candidate_fingerprint")) != expected_fingerprint:
            errors.append(f"{prefix}.candidate_fingerprint must match the integrated candidate")
        if not _is_iso_timestamp(item.get("observed_at")):
            errors.append(f"{prefix}.observed_at must be an offset-aware ISO-8601 timestamp")
        if _is_placeholder(item.get("observer")):
            errors.append(f"{prefix}.observer must be populated")
        if not _reference_is_acceptable(item.get("evidence_reference")):
            errors.append(f"{prefix}.evidence_reference must identify fresh non-synthetic external evidence")

    rollback = _as_mapping(evidence.get("rollback"))
    if _text(rollback.get("rolled_back_to_digest")) != _text(candidate.get("prior_application_image_digest")):
        errors.append("rollback evidence must target the exact prior immutable application digest")
    if _text(rollback.get("post_rollback_health")) != "PASS":
        errors.append("rollback.post_rollback_health must be PASS")

    saturation = _as_mapping(evidence.get("saturation"))
    if not _reference_is_acceptable(saturation.get("workload_profile_reference")):
        errors.append("saturation.workload_profile_reference must identify the exercised workload profile")

    recovery = _as_mapping(evidence.get("recovery"))
    for field in ("observed_rpo", "observed_rto"):
        if _is_placeholder(recovery.get(field)):
            errors.append(f"recovery.{field} must be recorded")

    for evidence_class in REQUIRED_EVIDENCE_CLASSES:
        item = _as_mapping(evidence.get(evidence_class))
        if _text(item.get("candidate_fingerprint")) and _text(item.get("candidate_fingerprint")) != _text(
            candidate.get("candidate_fingerprint")
        ):
            errors.append(f"evidence.{evidence_class} is mixed-candidate evidence")

    environment_id = _text(environment.get("environment_id"))
    if _is_placeholder(environment_id):
        errors.append("evidence cannot be accepted without one production-equivalent environment identity")


def _validate_review_and_claim_boundary(manifest: dict[str, Any], errors: list[str]) -> None:
    if manifest.get("release_blocking_findings_open") is not False:
        errors.append("release_blocking_findings_open must be false for Phase 11.10 acceptance")

    deviations = manifest.get("deviations")
    if not isinstance(deviations, list):
        errors.append("deviations must be a list")
    else:
        for index, deviation in enumerate(deviations):
            item = _as_mapping(deviation)
            if _is_placeholder(item.get("description")):
                errors.append(f"deviations[{index}].description must be populated")
            if _text(item.get("disposition")) not in {"ACCEPTED", "CLOSED"}:
                errors.append(f"deviations[{index}].disposition must be ACCEPTED or CLOSED")
            if _is_placeholder(item.get("owner")):
                errors.append(f"deviations[{index}].owner must be populated")

    review = _as_mapping(manifest.get("review"))
    if _text(review.get("decision")) != "PASS / OWNER_ACCEPTED":
        errors.append("review.decision must be PASS / OWNER_ACCEPTED")
    if _is_placeholder(review.get("reviewer")):
        errors.append("review.reviewer must be populated")
    if not _is_iso_timestamp(review.get("reviewed_at")):
        errors.append("review.reviewed_at must be an offset-aware ISO-8601 timestamp")
    if not _reference_is_acceptable(review.get("acceptance_reference")):
        errors.append("review.acceptance_reference must identify the accountable acceptance record")

    boundary = _as_mapping(manifest.get("claim_boundary"))
    if boundary.get("repository_ci_is_live_environment_evidence") is not False:
        errors.append("repository CI must not be represented as live environment evidence")
    if boundary.get("historical_phase8_9_evidence_reused") is not False:
        errors.append("historical Phase 8/9 evidence must not be reused")
    if boundary.get("production_authorized") is not False:
        errors.append("Phase 11.10 acceptance does not itself authorize production")


def validate_manifest(manifest: dict[str, Any]) -> dict[str, object]:
    errors: list[str] = []
    expected_fingerprint = _validate_identity(manifest, errors)
    _validate_evidence(manifest, expected_fingerprint, errors)
    _validate_review_and_claim_boundary(manifest, errors)
    return {
        "phase": "11.10",
        "manifest_valid": not errors,
        "phase11_10_acceptance_contract_satisfied": not errors,
        "candidate_fingerprint": expected_fingerprint,
        "required_evidence_classes": list(REQUIRED_EVIDENCE_CLASSES),
        "errors": errors,
        "production_authorized": False,
        "phase11_11_may_start": not errors,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Phase 11.10 evidence manifest must be a JSON object")
    return value


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the DTMO Phase 11.10 evidence contract")
    parser.add_argument(
        "--manifest",
        type=Path,
        help="validate a populated production-equivalent evidence manifest; omit to print the contract",
    )
    parser.add_argument(
        "--fingerprint",
        type=Path,
        help="calculate the candidate fingerprint for a partially populated manifest without claiming acceptance",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.manifest and args.fingerprint:
        raise SystemExit("use either --manifest or --fingerprint, not both")

    if args.fingerprint:
        manifest = load_manifest(args.fingerprint)
        print(json.dumps({"candidate_fingerprint": calculate_candidate_fingerprint(manifest)}, indent=2, sort_keys=True))
        return

    if args.manifest:
        try:
            manifest = load_manifest(args.manifest)
            report = validate_manifest(manifest)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            report = {
                "phase": "11.10",
                "manifest_valid": False,
                "phase11_10_acceptance_contract_satisfied": False,
                "errors": [str(exc)],
                "production_authorized": False,
                "phase11_11_may_start": False,
            }
        print(json.dumps(report, indent=2, sort_keys=True))
        if not report["manifest_valid"]:
            sys.exit(1)
        return

    print(json.dumps(build_contract(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
