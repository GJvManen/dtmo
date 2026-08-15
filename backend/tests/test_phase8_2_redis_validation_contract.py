from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/staging/PHASE8_2_REDIS_VALIDATION.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"
TEMPLATE = ROOT / "docs/staging/PHASE8_2_PLATFORM_IDENTITY_EVIDENCE.template.json"


def test_redis_runbook_preserves_external_evidence_boundary() -> None:
    text = RUNBOOK.read_text(encoding="utf-8")
    assert "Phase 8.2.4" in text
    assert "owner-approved post-E8 production-equivalent staging deployment" in text
    assert "same immutable Phase 8.2 deployment identity" in text
    assert "no production credentials are reused" in text
    assert "expiry/TTL" in text
    assert "fails safely" in text
    assert "Repository CI, Docker Compose, emulators and synthetic fixtures are supporting evidence only" in text
    assert "--check redis_coordination" in text
    assert "phase8_2_pass" in text
    assert "phase8_pass" in text


def test_redis_step_is_supported_by_manifest_and_validator() -> None:
    validator = VALIDATOR.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    assert '"redis_coordination"' in validator
    assert '"redis_coordination"' in template
