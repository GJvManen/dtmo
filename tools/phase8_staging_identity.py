#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

SHA40 = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")
FORBIDDEN_MARKERS = {"NOT_PROVIDED", "TODO", "TBD", "CHANGEME", "PLACEHOLDER"}
REQUIRED_TEXT = (
    "environment_id",
    "accountable_staging_owner",
    "approved_endpoint",
    "deployed_release",
    "deployed_commit",
    "application_image_digest",
    "configuration_parity_record",
    "tls_certificate_or_termination_evidence",
    "network_restriction_evidence",
    "data_class_and_sanitization_statement",
    "deployment_change_record",
    "rollback_target_and_procedure",
    "deployment_time_security_review",
)
REQUIRED_LISTS = (
    "supporting_container_digests",
    "infrastructure_runtime_inventory",
    "secrets_manager_identity_references",
    "least_privilege_staging_identities",
)


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _missing_or_placeholder(value: Any) -> bool:
    text = _text(value)
    return not text or text.upper() in FORBIDDEN_MARKERS


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_TEXT:
        if _missing_or_placeholder(manifest.get(key)):
            errors.append(f"{key}: required real staging evidence is missing")

    for key in REQUIRED_LISTS:
        value = manifest.get(key)
        if not isinstance(value, list) or not value:
            errors.append(f"{key}: expected a non-empty list")
        elif any(_missing_or_placeholder(item) for item in value):
            errors.append(f"{key}: contains an empty or placeholder value")

    commit = _text(manifest.get("deployed_commit"))
    if commit and not SHA40.fullmatch(commit):
        errors.append("deployed_commit: must be a full 40-character lowercase Git commit SHA")

    app_digest = _text(manifest.get("application_image_digest"))
    if app_digest and not DIGEST.fullmatch(app_digest):
        errors.append("application_image_digest: must be sha256:<64 lowercase hex characters>")

    supporting = manifest.get("supporting_container_digests")
    if isinstance(supporting, list):
        for index, digest in enumerate(supporting):
            if isinstance(digest, str) and not DIGEST.fullmatch(digest.strip()):
                errors.append(
                    f"supporting_container_digests[{index}]: must be sha256:<64 lowercase hex characters>"
                )

    endpoint = _text(manifest.get("approved_endpoint"))
    if endpoint:
        parsed = urlparse(endpoint)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append("approved_endpoint: must be an absolute https URL")

    if manifest.get("no_production_credentials_confirmation") is not True:
        errors.append("no_production_credentials_confirmation: must be true")

    if manifest.get("external_validation_authorized") is not True:
        errors.append("external_validation_authorized: must be true before validation starts")

    if manifest.get("phase8_pass") is True:
        errors.append("phase8_pass: must remain false; this tool validates identity intake only")

    if manifest.get("project_owner_staging_acceptance") not in (None, "NOT_RECORDED"):
        errors.append(
            "project_owner_staging_acceptance: must not be pre-populated by identity collection tooling"
        )

    return errors


def canonical_fingerprint(manifest: dict[str, Any]) -> str:
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be a JSON object")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a real Phase 8.1 staging deployment identity manifest."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args()

    try:
        manifest = load_manifest(args.manifest)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: unable to load manifest: {exc}", file=sys.stderr)
        return 2

    errors = validate_manifest(manifest)
    fingerprint = canonical_fingerprint(manifest)

    if args.json_output:
        print(
            json.dumps(
                {
                    "valid": not errors,
                    "phase8_pass": False,
                    "manifest_fingerprint": fingerprint,
                    "errors": errors,
                },
                indent=2,
                sort_keys=True,
            )
        )
    elif errors:
        print("PHASE 8.1 IDENTITY INTAKE: FAIL")
        for error in errors:
            print(f"- {error}")
        print(f"manifest_fingerprint: {fingerprint}")
    else:
        print("PHASE 8.1 IDENTITY INTAKE: PASS")
        print("Identity fields are syntactically coherent; external evidence still requires review.")
        print(f"manifest_fingerprint: {fingerprint}")
        print("phase8_pass: false")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
