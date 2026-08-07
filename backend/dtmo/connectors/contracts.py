from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Mapping, Sequence


_ALLOWED_AUTH_MODES = {"none", "environment"}
_ALLOWED_RELIABILITY = {"authoritative", "high", "medium", "low"}


@dataclass(frozen=True, slots=True)
class ConnectorContract:
    """Governance contract for a connector before any live execution is allowed."""

    connector_id: str
    source_url: str
    licence: str
    terms_url: str
    approved: bool
    source_reliability: str = "authoritative"
    confidence: int = 95
    auth_mode: str = "none"
    credential_env_names: tuple[str, ...] = ()
    timeout_seconds: float = 15.0
    max_attempts: int = 3
    minimum_interval_seconds: float = 2.0
    maximum_backoff_seconds: float = 30.0
    maximum_records: int = 2000
    quarantine_malformed: bool = True
    quarantine_duplicates: bool = True
    human_review_required: bool = True
    automatic_publication_allowed: bool = False
    provenance_notes: str = ""

    def validate_structure(self) -> list[str]:
        errors: list[str] = []
        if not self.connector_id.strip():
            errors.append("connector_id_required")
        if not self.source_url.startswith("https://"):
            errors.append("source_url_https_required")
        if not self.licence.strip():
            errors.append("licence_required")
        if not self.terms_url.startswith("https://"):
            errors.append("terms_url_https_required")
        if not self.approved:
            errors.append("connector_not_approved")
        if self.source_reliability not in _ALLOWED_RELIABILITY:
            errors.append("invalid_source_reliability")
        if not 0 <= self.confidence <= 100:
            errors.append("confidence_out_of_range")
        if self.auth_mode not in _ALLOWED_AUTH_MODES:
            errors.append("unsupported_auth_mode")
        if self.auth_mode == "none" and self.credential_env_names:
            errors.append("credentials_not_allowed_for_no_auth")
        if self.auth_mode == "environment" and not self.credential_env_names:
            errors.append("credential_names_required")
        if any(not name.strip() or "=" in name for name in self.credential_env_names):
            errors.append("invalid_credential_environment_name")
        if self.timeout_seconds <= 0:
            errors.append("timeout_must_be_positive")
        if not 1 <= self.max_attempts <= 5:
            errors.append("max_attempts_out_of_range")
        if self.minimum_interval_seconds < 0:
            errors.append("minimum_interval_negative")
        if not 0 < self.maximum_backoff_seconds <= 300:
            errors.append("maximum_backoff_out_of_range")
        if self.minimum_interval_seconds > self.maximum_backoff_seconds:
            errors.append("minimum_interval_exceeds_backoff")
        if not 1 <= self.maximum_records <= 5000:
            errors.append("maximum_records_out_of_range")
        if not self.quarantine_malformed:
            errors.append("malformed_quarantine_required")
        if not self.quarantine_duplicates:
            errors.append("duplicate_quarantine_required")
        if not self.human_review_required:
            errors.append("human_review_required")
        if self.automatic_publication_allowed:
            errors.append("automatic_publication_forbidden")
        return errors


@dataclass(frozen=True, slots=True)
class ConnectorContractEvidence:
    connector_id: str
    decision: str
    errors: tuple[str, ...]
    credential_requirements: tuple[str, ...]
    credentials_present: bool
    contract_digest: str
    publish_approved: bool = False

    def as_dict(self) -> dict[str, object]:
        return {
            "connector_id": self.connector_id,
            "decision": self.decision,
            "errors": list(self.errors),
            "credential_requirements": list(self.credential_requirements),
            "credentials_present": self.credentials_present,
            "contract_digest": self.contract_digest,
            "publish_approved": self.publish_approved,
        }


@dataclass(frozen=True, slots=True)
class ConnectorContractReport:
    evidence: tuple[ConnectorContractEvidence, ...]
    duplicate_connector_ids: tuple[str, ...] = field(default_factory=tuple)

    @property
    def decision(self) -> str:
        return "pass" if not self.duplicate_connector_ids and all(item.decision == "pass" for item in self.evidence) else "blocked"

    def as_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "decision": self.decision,
            "duplicate_connector_ids": list(self.duplicate_connector_ids),
            "connectors": [item.as_dict() for item in self.evidence],
            "publish_approved": False,
        }


def _contract_digest(contract: ConnectorContract) -> str:
    # Credential values are intentionally absent from the serialized governance contract.
    payload = {
        "connector_id": contract.connector_id,
        "source_url": contract.source_url,
        "licence": contract.licence,
        "terms_url": contract.terms_url,
        "approved": contract.approved,
        "source_reliability": contract.source_reliability,
        "confidence": contract.confidence,
        "auth_mode": contract.auth_mode,
        "credential_env_names": list(contract.credential_env_names),
        "timeout_seconds": contract.timeout_seconds,
        "max_attempts": contract.max_attempts,
        "minimum_interval_seconds": contract.minimum_interval_seconds,
        "maximum_backoff_seconds": contract.maximum_backoff_seconds,
        "maximum_records": contract.maximum_records,
        "quarantine_malformed": contract.quarantine_malformed,
        "quarantine_duplicates": contract.quarantine_duplicates,
        "human_review_required": contract.human_review_required,
        "automatic_publication_allowed": contract.automatic_publication_allowed,
        "provenance_notes": contract.provenance_notes,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def validate_connector_contracts(
    contracts: Sequence[ConnectorContract],
    *,
    environment: Mapping[str, str] | None = None,
) -> ConnectorContractReport:
    env = environment or {}
    counts: dict[str, int] = {}
    for contract in contracts:
        counts[contract.connector_id] = counts.get(contract.connector_id, 0) + 1
    duplicates = tuple(sorted(connector_id for connector_id, count in counts.items() if count > 1))

    results: list[ConnectorContractEvidence] = []
    for contract in contracts:
        errors = contract.validate_structure()
        credential_names = tuple(contract.credential_env_names)
        credentials_present = all(bool(env.get(name, "").strip()) for name in credential_names)
        if contract.auth_mode == "environment" and not credentials_present:
            errors.append("required_credentials_absent")
        if contract.connector_id in duplicates:
            errors.append("duplicate_connector_id")
        results.append(
            ConnectorContractEvidence(
                connector_id=contract.connector_id,
                decision="pass" if not errors else "blocked",
                errors=tuple(errors),
                credential_requirements=credential_names,
                credentials_present=credentials_present,
                contract_digest=_contract_digest(contract),
                publish_approved=False,
            )
        )
    return ConnectorContractReport(evidence=tuple(results), duplicate_connector_ids=duplicates)


def approved_cisa_kev_contract() -> ConnectorContract:
    return ConnectorContract(
        connector_id="cisa-kev-canary",
        source_url="https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        licence="US Government public domain",
        terms_url="https://www.cisa.gov/about/website-policies",
        approved=True,
        source_reliability="authoritative",
        confidence=95,
        auth_mode="none",
        timeout_seconds=15.0,
        max_attempts=3,
        minimum_interval_seconds=2.0,
        maximum_backoff_seconds=30.0,
        maximum_records=2000,
        quarantine_malformed=True,
        quarantine_duplicates=True,
        human_review_required=True,
        automatic_publication_allowed=False,
        provenance_notes="CISA KEV is the authoritative CISA catalog of vulnerabilities known to be exploited in the wild.",
    )
