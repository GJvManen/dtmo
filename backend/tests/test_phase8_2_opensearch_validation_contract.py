from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/staging/PHASE8_2_OPENSEARCH_VALIDATION.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"
TEMPLATE = ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json"


def test_opensearch_step_is_supported_by_phase8_validator() -> None:
    validator = VALIDATOR.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    assert '"opensearch_health_search"' in validator
    assert '"opensearch_health_search"' in template
    assert "--check" in validator


def test_opensearch_runbook_preserves_external_evidence_boundary() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "READY_FOR_EXTERNAL_EXECUTION / NOT_YET_ACCEPTED" in text
    assert "same immutable Phase 8.2 deployment identity" in text
    assert "canonical staged data" in text
    assert "no production credentials are reused" in text
    assert "fails safely" in text
    assert "--check opensearch_health_search" in text
    assert "cannot substitute for deployed-environment acceptance" in text
    assert "does not mark 8.2.1, 8.2.2, 8.2.3, Phase 8.2 or Phase 8 as `PASS`" in text
