from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = ROOT / "frontend" / "src" / "InvestigationsWorkspace.tsx"
ACCEPTANCE = ROOT / "docs" / "roadmap" / "FUNCTIONAL_RECOVERY_ACCEPTANCE.md"


def test_investigations_primary_flow_discovers_canonical_objects() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")

    # Phase 11.10q explicitly rejects manual UUID entry as a primary workflow.
    assert "Canonical intelligence item UUID" not in source
    assert 'placeholder="00000000-0000-0000-0000-000000000000"' not in source

    # Investigations must discover selectable persisted objects from the canonical
    # same-origin read model while preserving item deep links for object pivots.
    assert "/api/v1/command-center" in source
    assert "recent_intelligence" in source
    assert "Select" in source or "Open investigation" in source
    assert "new URLSearchParams(window.location.search).get('item')" in source
    assert "/api/v1/thehive/items/" in source


def test_investigation_discovery_does_not_expand_case_authority() -> None:
    source = WORKSPACE.read_text(encoding="utf-8")

    assert "handoff:case" in source
    assert "principal_actions.can_handoff" in source
    assert "external sharing" in source
    assert "No fabricated case detail" in source


def test_owner_acceptance_records_investigations_recovery_without_external_evidence_promotion() -> None:
    acceptance = ACCEPTANCE.read_text(encoding="utf-8")

    assert "MERGED / OWNER-AUTHORIZED MERGE" in acceptance
    assert "| Investigations | Normal/default workflow did not work. |" in acceptance
    assert "manual UUID is no longer the primary flow" in acceptance
    assert "Manual UUID entry is not an acceptable primary path" in acceptance
    assert "does **not** invent or retroactively create live, staging, production-equivalent" in acceptance
    assert "freeze a new candidate" in acceptance
