from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_integrated_analysis_runtime_contract_exists() -> None:
    api = read("backend/dtmo/intelowl_execution.py")
    persistence = read("backend/dtmo/persistence/cortex.py")
    migration = read("database/migrations/versions/0015_cortex_analysis_history.py")
    for marker in (
        '"/api/v1/analysis/capabilities"',
        '"/api/v1/analysis/items/{item_id}/cortex"',
        '"/api/v1/analysis/items/{item_id}/history"',
        "Permission.REVIEW_INTELLIGENCE",
        "CortexAnalysisRepository",
        "external_share_authority: bool = False",
        "local_compromise_proof: bool = False",
    ):
        assert marker in api
    for marker in (
        'external_share_authorized = false',
        'local_compromise_proven = false',
        'UniqueConstraint("item_id", "job_id"',
    ):
        assert marker in persistence
    assert 'revision: str = "0015_cortex_analysis_history"' in migration
    assert 'down_revision: str | None = "0014_thehive_handoff_state"' in migration


def test_analysis_workspace_preserves_human_authority_and_evidence_boundaries() -> None:
    app = read("frontend/src/App.tsx")
    workspace = read("frontend/src/AnalysisWorkspace.tsx")
    assert "<AnalysisWorkspace />" in app
    assert "11.10e Integrated Analysis" in workspace
    assert "review:intelligence required" in workspace
    assert "No responder authority" in workspace
    assert "Enrichment is evidence, not a verdict" in workspace
    assert "External share: no · Local compromise proven: no" in workspace
    assert "/api/v1/intelowl/items/" in workspace
    assert "/api/v1/analysis/items/" in workspace


def test_phase11_10e_documentation_status_remains_accepted_during_later_slice() -> None:
    current = read("docs/project/CURRENT_STATE.md")
    roadmap = read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    portal = read("docs/README.md")
    evidence = read("docs/evidence/EVIDENCE_INDEX.md")

    assert "Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10g MISP Sharing & Exchange | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10h TheHive Investigations & Cases | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10i Vulnerability & Exposure Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`" in current
    for text in (roadmap, portal, evidence):
        assert "11.10e" in text
        assert "11.10f" in text
        assert "11.10g" in text
        assert "11.10h" in text
        assert "11.10i" in text
    assert "not production authorized" in current.lower()
