from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNBOOK = ROOT / "docs/staging/PHASE8_2_OBJECT_STORAGE_VALIDATION.md"
VALIDATOR = ROOT / "tools/phase8_platform_validation.py"


def test_object_storage_runbook_binds_to_step_scoped_validator_and_same_identity() -> None:
    runbook = RUNBOOK.read_text(encoding="utf-8")
    validator = VALIDATOR.read_text(encoding="utf-8")

    assert "Phase 8.2.5" in runbook
    assert "object_storage_read_write" in runbook
    assert "--check object_storage_read_write" in runbook
    assert "same immutable staging deployment identity" in runbook
    assert "no production credentials" in runbook
    assert "Write a uniquely named disposable test object" in runbook
    assert "Read the object back" in runbook
    assert "Delete the test object" in runbook
    assert "fails safely" in runbook
    assert '"object_storage_read_write"' in validator


def test_object_storage_runbook_preserves_external_evidence_boundary() -> None:
    runbook = RUNBOOK.read_text(encoding="utf-8")

    assert "Repository CI" in runbook
    assert "supporting evidence only" in runbook
    assert "do not substitute" in runbook.lower()
    assert "restricted evidence reference" in runbook
    assert "Do not store raw credentials" in runbook
