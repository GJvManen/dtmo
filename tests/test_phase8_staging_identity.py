from __future__ import annotations

from copy import deepcopy

from tools.phase8_staging_identity import canonical_fingerprint, validate_manifest


VALID = {
    "environment_id": "staging-eu-west-001",
    "accountable_staging_owner": "security-platform-owner",
    "approved_endpoint": "https://staging.example.invalid",
    "deployed_release": "16.0.0rc12",
    "deployed_commit": "a" * 40,
    "application_image_digest": "sha256:" + "b" * 64,
    "supporting_container_digests": ["sha256:" + "c" * 64],
    "infrastructure_runtime_inventory": ["container-platform:cluster/staging-eu-west-001"],
    "configuration_parity_record": "evidence://phase8/config-parity/001",
    "secrets_manager_identity_references": ["secret-manager://staging/dtmo/app"],
    "least_privilege_staging_identities": ["iam://staging/dtmo-app"],
    "tls_certificate_or_termination_evidence": "evidence://phase8/tls/001",
    "network_restriction_evidence": "evidence://phase8/network/001",
    "data_class_and_sanitization_statement": "evidence://phase8/data/001",
    "no_production_credentials_confirmation": True,
    "deployment_change_record": "change://CHG-001",
    "rollback_target_and_procedure": "runbook://dtmo/staging-rollback",
    "deployment_time_security_review": "evidence://phase8/security-review/001",
    "external_validation_authorized": True,
    "project_owner_staging_acceptance": "NOT_RECORDED",
    "phase8_pass": False,
}


def test_valid_manifest_passes_identity_intake() -> None:
    assert validate_manifest(VALID) == []


def test_placeholder_and_missing_evidence_fail_closed() -> None:
    manifest = deepcopy(VALID)
    manifest["environment_id"] = "NOT_PROVIDED"
    manifest["supporting_container_digests"] = []
    errors = validate_manifest(manifest)
    assert any("environment_id" in error for error in errors)
    assert any("supporting_container_digests" in error for error in errors)


def test_requires_full_commit_digest_and_https_endpoint() -> None:
    manifest = deepcopy(VALID)
    manifest["deployed_commit"] = "abc123"
    manifest["application_image_digest"] = "latest"
    manifest["approved_endpoint"] = "http://staging.example.invalid"
    errors = validate_manifest(manifest)
    assert any("deployed_commit" in error for error in errors)
    assert any("application_image_digest" in error for error in errors)
    assert any("approved_endpoint" in error for error in errors)


def test_cannot_predeclare_phase8_pass_or_owner_acceptance() -> None:
    manifest = deepcopy(VALID)
    manifest["phase8_pass"] = True
    manifest["project_owner_staging_acceptance"] = "PASS"
    errors = validate_manifest(manifest)
    assert any("phase8_pass" in error for error in errors)
    assert any("project_owner_staging_acceptance" in error for error in errors)


def test_fingerprint_is_stable_across_key_order() -> None:
    reordered = dict(reversed(list(VALID.items())))
    assert canonical_fingerprint(VALID) == canonical_fingerprint(reordered)
