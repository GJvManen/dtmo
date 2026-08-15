from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/staging/PHASE8_2_POSTGRES_VALIDATION.md"


def test_postgres_runbook_is_external_identity_bound_and_fail_closed() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "READY_FOR_EXTERNAL_EXECUTION" in text
    assert "owner-approved production-equivalent staging deployment" in text
    assert "same immutable deployment identity" in text
    assert "current Alembic revision" in text
    assert "expected repository migration head" in text
    assert "does not rely on production credentials" in text
    assert "--check postgres_connectivity_migrations" in text
    assert "cannot substitute for this deployed-environment check" in text
    assert "8.2.3 — OpenSearch health/search" in text
