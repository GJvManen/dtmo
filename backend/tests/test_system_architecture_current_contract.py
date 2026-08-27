from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs/architecture/SYSTEM_ARCHITECTURE.md"


def test_system_architecture_reflects_current_integrated_recovery_baseline():
    text = ARCH.read_text(encoding="utf-8")
    for marker in (
        "AIL",
        "Cortex",
        "Unified Operations Workbench",
        "FUNCTIONAL RECOVERY ACTIVE",
        "Current external-owner functional acceptance",
        "NO-GO / REJECTED",
        "Phase 11.10p fresh production-equivalent execution",
        "BLOCKED BY FUNCTIONAL REJECTION",
        "Phase 11.11 independent external assurance",
        "NOT STARTED",
    ):
        assert marker in text, marker


def test_system_architecture_preserves_authority_and_evidence_boundaries():
    text = ARCH.read_text(encoding="utf-8").lower()
    for marker in (
        "server-side rbac",
        "human review/share",
        "server-side credentials",
        "repository ci",
        "not production authorized",
    ):
        assert marker in text, marker
