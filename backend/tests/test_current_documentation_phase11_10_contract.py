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

CANDIDATE_COMPLETION_SURFACES = tuple(path for path in CURRENT_SURFACES if path != "docs/security/SECURITY_OVERVIEW.md")

STALE_ACTIVE_MARKERS = (
    "Phase 11.10a frontend architecture/design contract | `IN PROGRESS / REPOSITORY ARCHITECTURE CONTRACT`",
    "Phase 11.10b canonical application shell | `NOT STARTED`",
    "11.10a frontend architecture/design contract — active",
    "active bounded objective is now **Phase 11.10a",
    "active bounded step is **Phase 11.10a",
    "Exactly one current priority: **complete PR #299",
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


def test_phase11_10b_candidate_completion_truth_is_professionally_reconciled() -> None:
    for path in CANDIDATE_COMPLETION_SURFACES:
        text = _read(path)
        assert "11.10a" in text, f"Phase 11.10a missing from {path}"
        assert "11.10b" in text, f"Phase 11.10b missing from {path}"
        assert "11.10p" in text, f"Phase 11.10p boundary missing from {path}"
        assert "production" in text.lower(), path

    current = _read("docs/project/CURRENT_STATE.md")
    for marker in (
        "Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10b canonical application shell | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 11.10c Command Center | `NOT STARTED`",
        "Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED`",
    ):
        assert marker in current, marker

    roadmap = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    for marker in (
        "11.10a Frontend architecture and design contract",
        "11.10b Canonical application shell",
        "11.10c Command Center",
        "11.10p Fresh production-equivalent validation",
    ):
        assert marker in roadmap, marker


def test_phase11_10b_application_shell_package_is_professionally_discoverable() -> None:
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

    portal = _read("docs/README.md")
    evidence = _read("docs/evidence/EVIDENCE_INDEX.md")
    qa = _read("docs/qa/QA_AND_RELEASE_GATES.md")

    for marker in (
        "architecture/PHASE11_10B_APPLICATION_SHELL.md",
        "qa/PHASE11_10B_APPLICATION_SHELL_GATE.md",
        "phase11-application-shell.yml",
        "frontend/package.json",
    ):
        assert marker in portal or marker in evidence or marker in qa, marker

    combined = portal + "\n" + evidence + "\n" + qa
    for marker in (
        "browser → DTMO API → governed integration adapter → upstream service",
        "server-side RBAC",
        "compatibility path",
        "does not prove",
    ):
        assert marker.lower() in combined.lower(), marker


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
