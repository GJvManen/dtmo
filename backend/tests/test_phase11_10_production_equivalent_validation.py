from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from tools.phase11_production_equivalent_validation import (
    REQUIRED_EVIDENCE_CLASSES,
    build_contract,
    calculate_candidate_fingerprint,
    validate_manifest,
)

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "docs" / "evidence" / "PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json"


def _valid_manifest() -> dict[str, object]:
    manifest: dict[str, object] = {
        "schema_version": "1.0",
        "phase": "11.10",
        "environment": {
            "environment_id": "pe-dtmo-01",
            "environment_class": "production-equivalent",
            "accountable_owner": "release-owner",
            "validation_operator": "validation-operator",
            "security_release_reviewer": "security-reviewer",
        },
        "candidate": {
            "deployed_commit": "1" * 40,
            "application_image_digest": "sha256:" + "2" * 64,
            "supporting_image_digests": ["sha256:" + "3" * 64, "sha256:" + "4" * 64],
            "migration_head": "0021_phase11_integrated_candidate",
            "deployment_revision": "gitops-rev-20260820-01",
            "prior_application_image_digest": "sha256:" + "5" * 64,
            "candidate_fingerprint": "",
        },
        "validation_window": {
            "started_at": "2026-08-20T09:00:00+02:00",
            "completed_at": "2026-08-20T11:30:00+02:00",
        },
        "evidence": {},
        "deviations": [],
        "release_blocking_findings_open": False,
        "review": {
            "decision": "PASS / OWNER_ACCEPTED",
            "reviewer": "accountable-owner",
            "reviewed_at": "2026-08-20T12:00:00+02:00",
            "acceptance_reference": "restricted-evidence://phase11-10/acceptance/01",
        },
        "claim_boundary": {
            "repository_ci_is_live_environment_evidence": False,
            "historical_phase8_9_evidence_reused": False,
            "production_authorized": False,
        },
    }
    fingerprint = calculate_candidate_fingerprint(manifest)
    candidate = manifest["candidate"]
    assert isinstance(candidate, dict)
    candidate["candidate_fingerprint"] = fingerprint

    evidence: dict[str, object] = {}
    for evidence_class in REQUIRED_EVIDENCE_CLASSES:
        evidence[evidence_class] = {
            "status": "PASS",
            "candidate_fingerprint": fingerprint,
            "observed_at": "2026-08-20T10:00:00+02:00",
            "observer": "validation-operator",
            "evidence_reference": f"restricted-evidence://phase11-10/{evidence_class}/01",
        }
    rollback = evidence["rollback"]
    assert isinstance(rollback, dict)
    rollback["rolled_back_to_digest"] = "sha256:" + "5" * 64
    rollback["post_rollback_health"] = "PASS"
    saturation = evidence["saturation"]
    assert isinstance(saturation, dict)
    saturation["workload_profile_reference"] = "restricted-evidence://phase11-10/workload/01"
    recovery = evidence["recovery"]
    assert isinstance(recovery, dict)
    recovery["observed_rpo"] = "0s observed for exercised path"
    recovery["observed_rto"] = "180s observed for exercised path"
    manifest["evidence"] = evidence
    return manifest


def test_phase11_10_requires_fresh_candidate_bound_evidence() -> None:
    contract = build_contract()
    assert contract["phase"] == "11.10"
    assert contract["status"] == "IN_PROGRESS"
    assert contract["historical_phase8_evidence_reusable"] is False
    assert contract["fresh_candidate_bound_evidence_required"] is True
    assert contract["missing_or_ambiguous_evidence"] == "FAIL_CLOSED"
    assert contract["production_authorized"] is False


def test_phase11_10_requires_complete_integrated_evidence_set() -> None:
    contract = build_contract()
    required = set(contract["required_evidence_classes"])
    assert required == set(REQUIRED_EVIDENCE_CLASSES)
    assert contract["same_candidate_required_for_phase11_11"] is True
    assert contract["final_manifest_decision"] == "PASS / OWNER_ACCEPTED"


def test_phase11_10_template_fails_closed_until_real_evidence_is_supplied() -> None:
    template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    report = validate_manifest(template)
    assert report["manifest_valid"] is False
    assert report["phase11_11_may_start"] is False
    assert report["production_authorized"] is False
    assert report["errors"]


def test_phase11_10_complete_single_candidate_manifest_satisfies_contract() -> None:
    report = validate_manifest(_valid_manifest())
    assert report["manifest_valid"] is True
    assert report["phase11_10_acceptance_contract_satisfied"] is True
    assert report["phase11_11_may_start"] is True
    assert report["production_authorized"] is False
    assert report["errors"] == []


def test_phase11_10_rejects_mixed_candidate_evidence() -> None:
    manifest = _valid_manifest()
    evidence = manifest["evidence"]
    assert isinstance(evidence, dict)
    health = evidence["health"]
    assert isinstance(health, dict)
    health["candidate_fingerprint"] = "sha256:" + "9" * 64
    report = validate_manifest(manifest)
    assert report["manifest_valid"] is False
    assert any("health" in error and "candidate_fingerprint" in error for error in report["errors"])


def test_phase11_10_rejects_historical_or_synthetic_evidence_reuse() -> None:
    for reference in (
        "restricted-evidence://phase8/historical-health",
        "repository CI synthetic fixture",
        "http://localhost:8000/evidence",
    ):
        manifest = _valid_manifest()
        evidence = manifest["evidence"]
        assert isinstance(evidence, dict)
        health = evidence["health"]
        assert isinstance(health, dict)
        health["evidence_reference"] = reference
        report = validate_manifest(manifest)
        assert report["manifest_valid"] is False
        assert any("health.evidence_reference" in error for error in report["errors"])


def test_phase11_10_rejects_rollback_to_wrong_digest_or_missing_post_health() -> None:
    manifest = _valid_manifest()
    evidence = manifest["evidence"]
    assert isinstance(evidence, dict)
    rollback = evidence["rollback"]
    assert isinstance(rollback, dict)
    rollback["rolled_back_to_digest"] = "sha256:" + "8" * 64
    rollback["post_rollback_health"] = "FAIL"
    report = validate_manifest(manifest)
    assert report["manifest_valid"] is False
    assert any("exact prior immutable" in error for error in report["errors"])
    assert any("post_rollback_health" in error for error in report["errors"])


def test_phase11_10_candidate_fingerprint_changes_with_identity_material() -> None:
    manifest = _valid_manifest()
    baseline = calculate_candidate_fingerprint(manifest)
    changed = deepcopy(manifest)
    candidate = changed["candidate"]
    assert isinstance(candidate, dict)
    candidate["deployment_revision"] = "gitops-rev-20260820-02"
    assert calculate_candidate_fingerprint(changed) != baseline
