from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs" / "architecture" / "THEHIVE_DTMO_HANDOFF_CONTRACT.md"
ROADMAP = ROOT / "docs" / "roadmap" / "PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs" / "project" / "CURRENT_STATE.md"
CONTRACT_GATE = ROOT / ".github" / "workflows" / "phase11-thehive-handoff-contract.yml"
IMPLEMENTATION_GATE = ROOT / ".github" / "workflows" / "phase11-thehive-handoff-implementation.yml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_thehive_handoff_contract_exists_and_is_bounded() -> None:
    text = _read(CONTRACT)
    for marker in (
        "TheHive",
        "case",
        "incident",
        "human",
        "approval",
        "provenance",
        "RBAC",
        "fail closed",
        "ambiguous",
        "does not make unrelated DTMO read paths unavailable",
    ):
        assert marker in text


def test_phase11_status_preserves_accepted_thehive_and_cortex_history() -> None:
    roadmap = _read(ROADMAP)
    state = _read(CURRENT_STATE)
    assert "11.5 MISP consolidation" in roadmap
    assert "11.6 TheHive incident/case handoff" in roadmap
    assert "11.7 Cortex decision gate" in roadmap
    assert "**Status:** `PASS / REPOSITORY_COMPLETE`" in roadmap
    assert "Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE`" in state
    assert "Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE`" in state
    # Preserve accepted 11.7/11.7b evidence while Phase 11.8 advances.
    assert (
        "Phase 11.7 Cortex decision gate | "
        "`PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`"
    ) in state
    assert "Phase 11.7b Cortex analyzer connector | `PASS / REPOSITORY_COMPLETE`" in state
    # 11.8a is accepted history; 11.8b is the sole active bounded slice.
    assert "Phase 11.8a runtime foundation | `PASS / REPOSITORY_COMPLETE`" in state
    assert (
        "Phase 11.8b workload identity / external secrets | "
        "`IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`"
    ) in state
    assert CONTRACT_GATE.exists()
    assert IMPLEMENTATION_GATE.exists()
