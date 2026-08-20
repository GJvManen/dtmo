from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

CURRENT_SURFACES = (
    "README.md",
    "docs/README.md",
    "docs/project/CURRENT_STATE.md",
    "docs/project/EXECUTIVE_STATUS.md",
    "docs/project/EXECUTIVE_DECISION_VIEW.md",
    "docs/project/PRODUCTION_READINESS_REPORT.md",
    "docs/project/PRODUCTION_CHECKLIST.md",
    "docs/project/DOCUMENTATION_STATUS.md",
    "docs/evidence/EVIDENCE_INDEX.md",
    "docs/qa/QA_AND_RELEASE_GATES.md",
    "docs/roadmap/PRODUCTION_ROADMAP.md",
    "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md",
    "docs/security/SECURITY_OVERVIEW.md",
)

CANDIDATE_COMPLETION_SURFACES = tuple(
    path for path in CURRENT_SURFACES if path != "docs/security/SECURITY_OVERVIEW.md"
)

STALE_ACTIVE_MARKERS = (
    "Phase 11.10a frontend architecture/design contract | `IN PROGRESS / REPOSITORY ARCHITECTURE CONTRACT`",
    "Phase 11.10b canonical application shell | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "Phase 11.10c Command Center | `NOT STARTED`",
    "Phase 11.10c Command Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "Phase 11.10d Unified Intelligence Workspace | `NOT STARTED`",
    "Phase 11.10d Unified Intelligence Workspace | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "Phase 11.10e IntelOwl/Cortex integrated analysis | `NOT STARTED`",
    "Phase 11.10e IntelOwl/Cortex integrated analysis | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "current bounded priority is **Phase 11.10b",
    "sole active bounded objective is now **Phase 11.10b",
    "Continue only **Phase 11.10b",
    "current bounded priority is **Phase 11.10c",
    "sole active bounded objective is **Phase 11.10c",
    "Continue only **Phase 11.10c",
    "current bounded priority is **Phase 11.10d",
    "sole active bounded objective is **Phase 11.10d",
    "current bounded priority is **Phase 11.10e",
    "sole active bounded objective is **Phase 11.10e",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_all_current_surfaces_expose_active_phase11_10_truth() -> None:
    for path in CURRENT_SURFACES:
        text = _read(path)
        assert "Phase 11" in text, path
        assert "IN PROGRESS" in text, path
        assert "Phase 11.10" in text, path
        assert "FRESH CANDIDATE-BOUND EVIDENCE REQUIRED" in text, path
        assert "Phase 11.11" in text, path
        assert "NOT STARTED" in text, path
        assert "Phase 12" in text, path
        assert "production" in text.lower(), path
        for marker in STALE_ACTIVE_MARKERS:
            assert marker not in text, f"stale lifecycle marker {marker!r} remains in {path}"


def test_current_surfaces_preserve_prior_candidate_evidence_boundary() -> None:
    for path in CURRENT_SURFACES:
        text = _read(path)
        assert "Phase 8" in text, path
        assert "Phase 9" in text, path
        assert "Phase 10" in text, path
        assert "NO-GO / BLOCKED" in text, path
        assert "OWNER_ACCEPTED" in text, path
        assert "EXTERNAL_ASSURANCE_ACCEPTED" in text, path
        assert "REPOSITORY_COMPLETE" in text, path


def test_phase11_10f_candidate_completion_truth_is_professionally_reconciled() -> None:
    for path in CANDIDATE_COMPLETION_SURFACES:
        text = _read(path)
        for phase in ("11.10a", "11.10b", "11.10c", "11.10d", "11.10e", "11.10f", "11.10p"):
            assert phase in text, f"Phase {phase} missing from {path}"
        assert "production" in text.lower(), path

    current = _read("docs/project/CURRENT_STATE.md")
    for marker in (
        "Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10f OpenCTI graph/entity workspace | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 11.10g MISP Sharing & Exchange | `NOT STARTED`",
        "Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED`",
    ):
        assert marker in current, marker

    roadmap = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    for marker in (
        "11.10a Frontend architecture and design contract",
        "11.10b Canonical application shell",
        "11.10c Command Center",
        "11.10d Unified Intelligence Workspace",
        "11.10e IntelOwl/Cortex integrated analysis",
        "11.10f OpenCTI",
        "11.10g MISP",
        "11.10p Fresh production-equivalent validation",
    ):
        assert marker in roadmap, marker


def test_phase11_10f_opencti_graph_package_is_professionally_discoverable() -> None:
    required_paths = (
        "backend/dtmo/opencti_workspace.py",
        "frontend/src/OpenCTIGraphWorkspace.tsx",
        "frontend/src/opencti-graph.css",
        "docs/architecture/PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "docs/user/OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "docs/qa/PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md",
        "backend/tests/test_phase11_10f_opencti_graph_contract.py",
        "backend/tests/test_phase11_10f_opencti_graph_browser.py",
        ".github/workflows/phase11-opencti-graph-workspace.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path

    combined = "\n".join(
        _read(path)
        for path in (
            "docs/README.md",
            "docs/evidence/EVIDENCE_INDEX.md",
            "docs/qa/QA_AND_RELEASE_GATES.md",
        )
    )
    for marker in (
        "PHASE11_10F_OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "OPENCTI_GRAPH_ENTITY_WORKSPACE.md",
        "PHASE11_10F_OPENCTI_GRAPH_ENTITY_GATE.md",
        "phase11-opencti-graph-workspace.yml",
    ):
        assert marker in combined, marker
    for marker in ("read-only", "fail closed", "does not prove", "production"):
        assert marker.lower() in combined.lower(), marker


def test_phase11_10e_integrated_analysis_package_remains_professionally_discoverable() -> None:
    required_paths = (
        "backend/dtmo/intelowl_execution.py",
        "backend/dtmo/persistence/cortex.py",
        "database/migrations/versions/0015_cortex_analysis_history.py",
        "frontend/src/AnalysisWorkspace.tsx",
        "frontend/src/analysis-workspace.css",
        "docs/architecture/PHASE11_10E_INTEGRATED_ANALYSIS_WORKSPACE.md",
        "docs/user/INTEGRATED_ANALYSIS_WORKSPACE.md",
        "docs/qa/PHASE11_10E_INTEGRATED_ANALYSIS_GATE.md",
        "backend/tests/test_phase11_10e_integrated_analysis_contract.py",
        "backend/tests/test_phase11_10e_integrated_analysis_browser.py",
        ".github/workflows/phase11-integrated-analysis-workspace.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path


def test_phase11_10d_unified_intelligence_package_remains_professionally_discoverable() -> None:
    required_paths = (
        "frontend/src/UnifiedIntelligenceWorkspace.tsx",
        "frontend/src/unified-intelligence.css",
        "docs/architecture/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE.md",
        "docs/user/UNIFIED_INTELLIGENCE_WORKSPACE.md",
        "docs/qa/PHASE11_10D_UNIFIED_INTELLIGENCE_WORKSPACE_GATE.md",
        "backend/tests/test_phase11_10d_unified_intelligence_workspace_contract.py",
        "backend/tests/test_phase11_10d_unified_intelligence_workspace_browser.py",
        ".github/workflows/phase11-unified-intelligence-workspace.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path


def test_phase11_10c_command_center_package_remains_professionally_discoverable() -> None:
    required_paths = (
        "backend/dtmo/command_center.py",
        "backend/dtmo/api_command_center.py",
        "frontend/src/App.tsx",
        "frontend/src/command-center.css",
        "docs/architecture/PHASE11_10C_COMMAND_CENTER.md",
        "docs/qa/PHASE11_10C_COMMAND_CENTER_GATE.md",
        "backend/tests/test_phase11_10c_command_center_contract.py",
        "backend/tests/test_phase11_10c_command_center_browser.py",
        ".github/workflows/phase11-command-center.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path


def test_phase11_10b_application_shell_package_remains_discoverable() -> None:
    required_paths = (
        "frontend/package.json",
        "frontend/src/main.tsx",
        "frontend/src/App.tsx",
        "frontend/src/styles.css",
        "backend/dtmo/workbench_frontend.py",
        "docs/architecture/PHASE11_10B_APPLICATION_SHELL.md",
        "docs/qa/PHASE11_10B_APPLICATION_SHELL_GATE.md",
        "backend/tests/test_phase11_10b_application_shell_contract.py",
        "backend/tests/test_phase11_10b_application_shell_browser.py",
        ".github/workflows/phase11-application-shell.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path


def test_phase11_10a_architecture_baseline_remains_discoverable() -> None:
    for path in (
        "docs/architecture/FRONTEND_ARCHITECTURE.md",
        "docs/architecture/UI_API_CONTRACT.md",
        "docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md",
        "docs/ux/INFORMATION_ARCHITECTURE.md",
        "docs/ux/DESIGN_SYSTEM.md",
        "docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md",
        ".github/workflows/phase11-frontend-architecture.yml",
    ):
        assert (ROOT / path).is_file(), path


def test_phase11_10_execution_package_is_professionally_discoverable() -> None:
    required_paths = (
        "docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md",
        "docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md",
        "docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json",
        "tools/phase11_production_equivalent_validation.py",
        "backend/tests/test_phase11_10_production_equivalent_validation.py",
        ".github/workflows/phase11-production-equivalent-validation.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path

    portal = _read("docs/README.md")
    evidence = _read("docs/evidence/EVIDENCE_INDEX.md")
    current = _read("docs/project/CURRENT_STATE.md")
    root_readme = _read("README.md")
    for marker in (
        "PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md",
        "PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json",
        "phase11_production_equivalent_validation.py",
        "phase11-production-equivalent-validation.yml",
    ):
        assert marker in portal or marker in root_readme, marker
        assert marker in evidence, marker
        assert marker in current or marker in evidence, marker


def test_phase11_10_professional_claim_boundary_remains_fail_closed() -> None:
    combined = "\n".join(_read(path) for path in CURRENT_SURFACES)
    for marker in (
        "historical",
        "same immutable",
        "fail closed",
        "repository CI",
        "not production authorized",
    ):
        assert marker.lower() in combined.lower(), marker

    gate = _read("docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md")
    runbook = _read("docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md")
    for marker in (
        "exact prior immutable",
        "post-rollback health",
        "automatic database down migration",
        "PASS / OWNER_ACCEPTED",
    ):
        assert marker.lower() in gate.lower(), marker
        assert marker.lower() in runbook.lower(), marker
