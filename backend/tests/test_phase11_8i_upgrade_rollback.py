from pathlib import Path

import pytest

from tools.phase11_upgrade_rollback_exercise import build_evidence


ROOT = Path(__file__).resolve().parents[2]
VALUES = ROOT / "deploy/helm/dtmo/values.yaml"
RUNTIME = ROOT / "deploy/helm/dtmo/templates/runtime.yaml"
ARCH = ROOT / "docs/architecture/PHASE11_8I_UPGRADE_ROLLBACK.md"
RUNBOOK = ROOT / "docs/operations/PHASE11_8I_UPGRADE_ROLLBACK_RUNBOOK.md"
QA = ROOT / "docs/qa/PHASE11_8I_UPGRADE_ROLLBACK_GATE.md"


BASELINE = "sha256:" + "1" * 64
CANDIDATE = "sha256:" + "2" * 64
HEAD = "a" * 40


def test_upgrade_policy_is_explicit_and_fail_closed() -> None:
    values = VALUES.read_text(encoding="utf-8")
    runtime = RUNTIME.read_text(encoding="utf-8")

    for required in (
        "maxUnavailable: 0",
        "maxSurge: 1",
        "revisionHistoryLimit: 5",
        "progressDeadlineSeconds: 600",
        "minReadySeconds: 10",
        "requirePriorImmutableDigest: true",
        "requirePostRollbackHealthEvidence: true",
        "forbidAutomaticDatabaseDownMigration: true",
    ):
        assert required in values

    for required in (
        "upgrade.strategy.maxUnavailable must remain 0",
        "upgrade.strategy.maxSurge must be at least 1",
        "upgrade.revisionHistoryLimit must preserve at least two revisions",
        "revisionHistoryLimit: {{ .Values.upgrade.revisionHistoryLimit }}",
        "progressDeadlineSeconds: {{ .Values.upgrade.progressDeadlineSeconds }}",
        "minReadySeconds: {{ .Values.upgrade.minReadySeconds }}",
    ):
        assert required in runtime


def test_repository_exercise_returns_to_exact_prior_digest() -> None:
    evidence = build_evidence(baseline=BASELINE, candidate=CANDIDATE, exact_head=HEAD)
    assert evidence["decision"] == "pass"
    assert evidence["upgrade_transition"] == [BASELINE, CANDIDATE]
    assert evidence["rollback_transition"] == [CANDIDATE, BASELINE]
    assert evidence["rollback_digest"] == BASELINE
    assert evidence["rollback_restores_exact_prior_digest"] is True
    assert evidence["automatic_database_down_migration_allowed"] is False
    assert evidence["post_rollback_health_evidence_required"] is True
    assert evidence["production_equivalent_exercise_claimed"] is False
    assert evidence["live_cluster_rollback_claimed"] is False
    assert evidence["production_authorization_claimed"] is False


def test_exercise_rejects_mutable_or_non_exercise_inputs() -> None:
    with pytest.raises(ValueError, match="immutable sha256"):
        build_evidence(baseline="latest", candidate=CANDIDATE, exact_head=HEAD)
    with pytest.raises(ValueError, match="actually exercised"):
        build_evidence(baseline=BASELINE, candidate=BASELINE, exact_head=HEAD)


def test_professional_upgrade_rollback_documentation_contract() -> None:
    docs = "\n".join(
        path.read_text(encoding="utf-8") for path in (ARCH, RUNBOOK, QA)
    ).lower()
    for phrase in (
        "upgrade",
        "rollback",
        "immutable digest",
        "health evidence",
        "database down migration",
        "fail closed",
        "phase 11.10",
        "production authorization",
    ):
        assert phrase in docs
