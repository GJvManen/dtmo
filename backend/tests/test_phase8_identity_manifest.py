from argparse import Namespace

import pytest

from tools.phase8_identity_manifest import build_manifest


def _args(**overrides: object) -> Namespace:
    values: dict[str, object] = {
        "environment_id": "staging-approved-01",
        "owner": "accountable-owner-ref",
        "endpoint": "https://staging.example.test",
        "release": "16.0.0rc12-post-e8",
        "commit": "a" * 40,
        "application_digest": "sha256:" + "b" * 64,
        "supporting_digest": ["sha256:" + "c" * 64],
        "runtime_inventory_ref": "evidence/runtime-inventory-01",
        "configuration_parity_ref": "evidence/config-parity-01",
        "secrets_identity_ref": "secret-manager://staging/dtmo-identities",
        "least_privilege_ref": "evidence/iam-separation-01",
        "tls_network_ref": "evidence/tls-network-01",
        "data_sanitization_ref": "evidence/data-sanitization-01",
        "no_prod_credentials_ref": "evidence/no-prod-credentials-01",
        "change_record_ref": "change/CHG-1001",
        "rollback_record_ref": "change/CHG-1001-rollback",
        "security_review_ref": "evidence/security-review-01",
    }
    values.update(overrides)
    return Namespace(**values)


def test_manifest_accepts_explicit_immutable_identity_values() -> None:
    manifest = build_manifest(_args())
    assert manifest.environment_id == "staging-approved-01"
    assert manifest.deployed_commit == "a" * 40
    assert manifest.application_image_digest.startswith("sha256:")
    assert manifest.phase8_pass is False
    assert manifest.evidence_classification == "external-staging-identity-binding"


@pytest.mark.parametrize("value", ["", "NOT_PROVIDED", "UNKNOWN", "TBD", "N/A"])
def test_manifest_fails_closed_on_placeholder_identity_values(value: str) -> None:
    with pytest.raises(ValueError):
        build_manifest(_args(environment_id=value))


def test_manifest_rejects_nonimmutable_commit() -> None:
    with pytest.raises(ValueError, match="40-character"):
        build_manifest(_args(commit="main"))


def test_manifest_rejects_mutable_image_reference() -> None:
    with pytest.raises(ValueError, match="sha256"):
        build_manifest(_args(application_digest="dtmo:latest"))


def test_manifest_requires_supporting_digests() -> None:
    with pytest.raises(ValueError, match="at least one supporting"):
        build_manifest(_args(supporting_digest=[]))
