from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_cortex_decision_requires_validated_gap_before_adoption() -> None:
    decision = _read("docs/architecture/CORTEX_DECISION_GATE.md")
    assert "does **not** adopt Cortex" in decision
    assert "no such validated gap" in decision
    assert "Re-entry criteria" in decision
    assert "publication/share authority" in decision
    assert "responders remain excluded" in decision


def test_decision_is_exposed_as_phase11_7_gate() -> None:
    qa = _read("docs/qa/PHASE11_7_CORTEX_DECISION_GATE.md")
    roadmap = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    portal = _read("docs/README.md")
    current = _read("docs/project/CURRENT_STATE.md")
    for text in (qa, roadmap, portal, current):
        assert "Phase 11.7" in text or "11.7" in text
    assert "CORTEX_DECISION_GATE.md" in portal
    assert "Phase 11.8" in decision_next_priority()


def decision_next_priority() -> str:
    return _read("docs/architecture/CORTEX_DECISION_GATE.md")
