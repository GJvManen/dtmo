from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
FORBIDDEN = {"", "NOT_PROVIDED", "UNKNOWN", "TBD", "N/A"}


@dataclass(frozen=True)
class Phase8IdentityManifest:
    environment_id: str
    accountable_staging_owner: str
    approved_endpoint: str
    deployed_release: str
    deployed_commit: str
    application_image_digest: str
    supporting_container_digests: list[str]
    infrastructure_runtime_inventory_ref: str
    configuration_parity_record_ref: str
    secrets_manager_identity_refs: str
    least_privilege_staging_identities_ref: str
    tls_network_evidence_ref: str
    data_sanitization_statement_ref: str
    no_production_credentials_confirmation_ref: str
    deployment_change_record_ref: str
    rollback_record_ref: str
    deployment_time_security_review_ref: str
    evidence_classification: str = "external-staging-identity-binding"
    phase8_pass: bool = False


def _required(name: str, value: str) -> str:
    cleaned = value.strip()
    if cleaned.upper() in FORBIDDEN:
        raise ValueError(f"{name} must be explicitly observed and may not be {value!r}")
    return cleaned


def _commit(value: str) -> str:
    value = _required("deployed_commit", value).lower()
    if not SHA_RE.fullmatch(value):
        raise ValueError("deployed_commit must be a full 40-character lowercase Git SHA")
    return value


def _digest(name: str, value: str) -> str:
    value = _required(name, value).lower()
    if not DIGEST_RE.fullmatch(value):
        raise ValueError(f"{name} must be an immutable sha256:<64 hex> digest")
    return value


def build_manifest(args: argparse.Namespace) -> Phase8IdentityManifest:
    supporting = [_digest("supporting_container_digest", item) for item in args.supporting_digest]
    if not supporting:
        raise ValueError("at least one supporting container digest is required")
    return Phase8IdentityManifest(
        environment_id=_required("environment_id", args.environment_id),
        accountable_staging_owner=_required("accountable_staging_owner", args.owner),
        approved_endpoint=_required("approved_endpoint", args.endpoint),
        deployed_release=_required("deployed_release", args.release),
        deployed_commit=_commit(args.commit),
        application_image_digest=_digest("application_image_digest", args.application_digest),
        supporting_container_digests=supporting,
        infrastructure_runtime_inventory_ref=_required("infrastructure_runtime_inventory_ref", args.runtime_inventory_ref),
        configuration_parity_record_ref=_required("configuration_parity_record_ref", args.configuration_parity_ref),
        secrets_manager_identity_refs=_required("secrets_manager_identity_refs", args.secrets_identity_ref),
        least_privilege_staging_identities_ref=_required("least_privilege_staging_identities_ref", args.least_privilege_ref),
        tls_network_evidence_ref=_required("tls_network_evidence_ref", args.tls_network_ref),
        data_sanitization_statement_ref=_required("data_sanitization_statement_ref", args.data_sanitization_ref),
        no_production_credentials_confirmation_ref=_required("no_production_credentials_confirmation_ref", args.no_prod_credentials_ref),
        deployment_change_record_ref=_required("deployment_change_record_ref", args.change_record_ref),
        rollback_record_ref=_required("rollback_record_ref", args.rollback_record_ref),
        deployment_time_security_review_ref=_required("deployment_time_security_review_ref", args.security_review_ref),
    )


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Create a fail-closed Phase 8 immutable staging identity manifest.")
    p.add_argument("--environment-id", required=True)
    p.add_argument("--owner", required=True)
    p.add_argument("--endpoint", required=True)
    p.add_argument("--release", required=True)
    p.add_argument("--commit", required=True)
    p.add_argument("--application-digest", required=True)
    p.add_argument("--supporting-digest", action="append", default=[])
    p.add_argument("--runtime-inventory-ref", required=True)
    p.add_argument("--configuration-parity-ref", required=True)
    p.add_argument("--secrets-identity-ref", required=True)
    p.add_argument("--least-privilege-ref", required=True)
    p.add_argument("--tls-network-ref", required=True)
    p.add_argument("--data-sanitization-ref", required=True)
    p.add_argument("--no-prod-credentials-ref", required=True)
    p.add_argument("--change-record-ref", required=True)
    p.add_argument("--rollback-record-ref", required=True)
    p.add_argument("--security-review-ref", required=True)
    p.add_argument("--output", type=Path, required=True)
    return p


def main() -> int:
    args = parser().parse_args()
    manifest = build_manifest(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote fail-closed Phase 8 identity manifest: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
