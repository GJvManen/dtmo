from pathlib import Path

PLAN = Path("docs/staging/STAGING_ACCEPTANCE_PLAN.md")
QA = Path("docs/qa/PHASE8_STAGING_READINESS_GATE.md")


def test_staging_plan_exists_and_is_fail_closed() -> None:
    text = PLAN.read_text(encoding="utf-8")
    required = [
        "production-equivalent",
        "immutable",
        "Secrets and identity",
        "TLS and network restrictions",
        "Smoke and integration",
        "Migration",
        "Connector acceptance",
        "Recovery",
        "Performance",
        "Accessibility/operational UX",
        "Observability/incident operations",
        "Security review",
        "human share approval",
        "No staging deployment or staging acceptance is claimed",
    ]
    for marker in required:
        assert marker in text


def test_staging_evidence_matrix_requires_exact_environment_evidence() -> None:
    text = PLAN.read_text(encoding="utf-8")
    for marker in [
        "environment identifier",
        "immutable artifact digests",
        "machine-readable result",
        "configuration parity record",
        "rollback/recovery result",
        "unresolved findings",
        "acceptance decision",
    ]:
        assert marker in text
    assert "missing, inaccessible, queued, cancelled, failed, stale-head" in text


def test_phase8_qa_preserves_accepted_readiness_and_current_external_claim_boundary() -> None:
    text = QA.read_text(encoding="utf-8")
    assert "**Decision:** `PASS`" in text
    assert "READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY" not in text
    assert "post-E8 candidate has been externally deployed and extensively tested" in text
    assert "owner-approved production-equivalent staging environment" in text
    assert "immutable deployment identity" in text
    assert "configuration parity/deviations" in text
    assert "IAM/secrets/least privilege" in text
    assert "Formal Phase 8 closure still requires" in text
    assert "accountable Phase 8.5 owner decision" in text
    assert "does not claim Phase 8 external acceptance" in text
    assert "Phase 9 independent assurance" in text
    assert "production approval" in text
    assert "Repository CI, local Docker Compose, staging emulators" in text
