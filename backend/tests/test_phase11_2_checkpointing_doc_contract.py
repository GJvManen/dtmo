from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def test_phase11_2_checkpointing_status_is_present_and_bounded() -> None:
    text = (ROOT / "docs/roadmap/PHASE11_2_CHECKPOINTING_STATUS.md").read_text(encoding="utf-8")
    assert "IMPLEMENTED / EXACT-HEAD VALIDATION REQUIRED" in text
    assert "durable checkpoint" in text.lower()
    assert "reconciliation" in text.lower()
    assert "production persistent volume" in text.lower()
    assert "Phase 11.3 IntelOwl" in text
