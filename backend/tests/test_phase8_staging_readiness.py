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


def test_phase8_qa_preserves_claim_boundary() -> None:
    text = QA.read_text(encoding="utf-8")
    assert "CI_VALIDATION_PENDING" in text
    assert "does not claim a staging environment exists" in text
    assert "staging tests have executed" in text
    assert "production acceptance is complete" in text
    assert "every registered workflow succeeds on the exact final head" in text
