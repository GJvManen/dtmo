from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_recovery_domains_and_fail_closed_boundaries_are_documented():
    architecture = read("docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md").lower()
    runbook = read("docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md").lower()
    gate = read("docs/qa/PHASE11_8F_RECOVERY_GATE.md").lower()
    for marker in ("postgresql", "redis", "opensearch", "object storage", "restore", "rpo", "rto", "fails closed"):
        assert marker in architecture or marker in gate
    assert "rollback" in runbook
    assert "does not prove" in gate


def test_recovery_contract_rejects_inferred_production_evidence():
    text = read("docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md").lower()
    assert "backup success is never inferred" in text
    assert "production authorization" in text
    assert "historical phase 8/9" not in text or "does not" in text
