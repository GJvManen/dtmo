from __future__ import annotations

import json

from dtmo.connectors.contracts import ConnectorContract, approved_cisa_kev_contract, validate_connector_contracts


def test_approved_cisa_contract_passes_without_credentials_and_never_approves_publication() -> None:
    report = validate_connector_contracts([approved_cisa_kev_contract()])

    assert report.decision == "pass"
    assert report.duplicate_connector_ids == ()
    evidence = report.evidence[0]
    assert evidence.decision == "pass"
    assert evidence.credentials_present is True
    assert evidence.publish_approved is False
    assert len(evidence.contract_digest) == 64
    assert report.as_dict()["publish_approved"] is False


def test_environment_credentials_are_presence_checked_without_secret_disclosure() -> None:
    contract = ConnectorContract(
        connector_id="vendor-advisory",
        source_url="https://vendor.example/advisories",
        licence="licensed-feed",
        terms_url="https://vendor.example/terms",
        approved=True,
        auth_mode="environment",
        credential_env_names=("VENDOR_API_TOKEN",),
    )
    test_token = "non-sensitive-test-token"  # noqa: S105 - fixture verifies evidence redaction, not a credential
    report = validate_connector_contracts([contract], environment={"VENDOR_API_TOKEN": test_token})

    assert report.decision == "pass"
    serialized = json.dumps(report.as_dict(), sort_keys=True)
    assert "VENDOR_API_TOKEN" in serialized
    assert test_token not in serialized


def test_missing_required_credentials_fail_closed() -> None:
    contract = ConnectorContract(
        connector_id="vendor-advisory",
        source_url="https://vendor.example/advisories",
        licence="licensed-feed",
        terms_url="https://vendor.example/terms",
        approved=True,
        auth_mode="environment",
        credential_env_names=("VENDOR_API_TOKEN",),
    )

    report = validate_connector_contracts([contract], environment={})

    assert report.decision == "blocked"
    assert "required_credentials_absent" in report.evidence[0].errors
    assert report.evidence[0].publish_approved is False


def test_duplicate_connector_ids_fail_closed() -> None:
    first = approved_cisa_kev_contract()
    second = approved_cisa_kev_contract()

    report = validate_connector_contracts([first, second])

    assert report.decision == "blocked"
    assert report.duplicate_connector_ids == ("cisa-kev-canary",)
    assert all("duplicate_connector_id" in evidence.errors for evidence in report.evidence)


def test_contract_requires_provenance_rate_controls_quarantine_and_human_review() -> None:
    unsafe = ConnectorContract(
        connector_id="unsafe",
        source_url="http://example.test/feed",
        licence="",
        terms_url="http://example.test/terms",
        approved=False,
        max_attempts=6,
        minimum_interval_seconds=31.0,
        maximum_backoff_seconds=30.0,
        quarantine_malformed=False,
        quarantine_duplicates=False,
        human_review_required=False,
        automatic_publication_allowed=True,
    )

    report = validate_connector_contracts([unsafe])

    assert report.decision == "blocked"
    errors = set(report.evidence[0].errors)
    assert {
        "source_url_https_required",
        "licence_required",
        "terms_url_https_required",
        "connector_not_approved",
        "max_attempts_out_of_range",
        "minimum_interval_exceeds_backoff",
        "malformed_quarantine_required",
        "duplicate_quarantine_required",
        "human_review_required",
        "automatic_publication_forbidden",
    } <= errors
    assert report.evidence[0].publish_approved is False
