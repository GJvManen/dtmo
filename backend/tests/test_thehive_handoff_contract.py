from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md"
CONTRACT_GATE = ROOT / "docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md"
IMPLEMENTATION_GATE = ROOT / "docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_thehive_contract_records_upstream_api_and_license_boundary() -> None:
    text = _read(CONTRACT)
    for marker in (
        "TheHive 5.5.16",
        "API v1 (`/api/v1`)",
        "POST /api/v1/case",
        "Community",
        "Gold",
        "Platinum",
        "does not vendor TheHive source",
    ):
        assert marker in text


def test_thehive_contract_preserves_human_authority_and_canonical_truth() -> None:
    text = _read(CONTRACT)
    for marker in (
        "never creates a TheHive case by itself",
        "human-authorized DTMO action",
        "Publication/share approval and case-handoff approval remain distinct authorities",
        "does not grant DTMO publication/share authority",
        "does not prove local compromise",
        "does not change canonical CTI truth",
    ):
        assert marker in text


def test_thehive_contract_is_fail_closed_and_idempotent() -> None:
    text = _read(CONTRACT)
    for marker in (
        "idempotency key",
        "cannot be automatically replayed",
        "TLP/PAP",
        "authentication/authorization/write-boundary rejection",
        "ambiguous",
        "does not make unrelated DTMO read paths unavailable",
    ):
        assert marker in text


def test_phase11_status_preserves_accepted_thehive_and_active_cortex_decision() -> None:
    roadmap = _read(ROADMAP)
    state = _read(CURRENT_STATE)
    assert "11.5 MISP consolidation" in roadmap
    assert "11.6 TheHive incident/case handoff" in roadmap
    assert "11.7 Cortex decision gate" in roadmap
    assert "**Status:** `PASS / REPOSITORY_COMPLETE`" in roadmap
    assert "Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE`" in state
    assert "Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE`" in state
    assert "Phase 11.7 Cortex decision gate | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`" in state
    assert CONTRACT_GATE.exists()
    assert IMPLEMENTATION_GATE.exists()
