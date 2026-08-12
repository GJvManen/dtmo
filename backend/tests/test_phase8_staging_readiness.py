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


def test_phase8_qa_preserves_accepted_readiness_and_external_claim_boundary() -> None:
    text = QA.read_text(encoding="utf-8")
    assert "**Decision:** `PASS`" in text
    assert "READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY" in text
    assert "immutable deployment identity" in text
    assert "configuration parity" in text
    assert "approved IAM/secrets references and least privilege" in text
    assert "It does **not** claim that:" in text
    assert "a production-equivalent staging environment has been provisioned" in text
    assert "external staging suites have executed" in text
    assert "Phase 8 is complete" in text
    assert "production deployment is approved" in text
    assert "PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md" in text
