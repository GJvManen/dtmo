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


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_all_current_surfaces_preserve_phase11_release_truth() -> None:
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
        assert "Phase 8" in text, path
        assert "Phase 9" in text, path
        assert "Phase 10" in text, path
        assert "NO-GO / BLOCKED" in text, path
        assert "OWNER_ACCEPTED" in text, path
        assert "EXTERNAL_ASSURANCE_ACCEPTED" in text, path
        assert "REPOSITORY_COMPLETE" in text, path


def test_phase11_10i_current_state_is_exact_and_fail_closed() -> None:
    current = _read("docs/project/CURRENT_STATE.md")
    for marker in (
        "Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10d Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10e IntelOwl/Cortex integrated analysis | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10f OpenCTI graph/entity workspace | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10g MISP Sharing & Exchange | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10h TheHive Investigations & Cases | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.10i Vulnerability & Exposure Center | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 11.10j Sources & Collection Control Center | `NOT STARTED`",
        "Phase 11.10p fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED`",
    ):
        assert marker in current, marker

    for stale in (
        "sole active bounded objective is **Phase 11.10h",
        "Phase 11.10h TheHive Investigations & Cases | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 11.10i Vulnerability & Exposure Center | `NOT STARTED`",
    ):
        assert stale not in current, stale

    for marker in (
        "CVSS",
        "EPSS",
        "KEV",
        "fail closed",
        "server-side RBAC",
        "repository CI",
        "not production authorized",
        "same immutable",
    ):
        assert marker.lower() in current.lower(), marker


def test_phase11_10i_package_is_professionally_discoverable() -> None:
    required_paths = (
        "frontend/src/ExposureWorkspace.tsx",
        "frontend/src/App.tsx",
        "docs/architecture/PHASE11_10I_VULNERABILITY_EXPOSURE.md",
        "docs/user/VULNERABILITY_EXPOSURE_WORKSPACE.md",
        "docs/qa/PHASE11_10I_VULNERABILITY_EXPOSURE_GATE.md",
        "backend/tests/test_phase11_10i_vulnerability_exposure_contract.py",
        ".github/workflows/phase11-vulnerability-exposure.yml",
    )
    for path in required_paths:
        assert (ROOT / path).is_file(), path

    combined = "\n".join(
        _read(path)
        for path in (
            "docs/project/CURRENT_STATE.md",
            "docs/architecture/PHASE11_10I_VULNERABILITY_EXPOSURE.md",
            "docs/user/VULNERABILITY_EXPOSURE_WORKSPACE.md",
            "docs/qa/PHASE11_10I_VULNERABILITY_EXPOSURE_GATE.md",
        )
    )
    for marker in (
        "PHASE11_10I_VULNERABILITY_EXPOSURE",
        "Vulnerability & Exposure",
        "CVSS",
        "EPSS",
        "KEV",
        "fail closed",
        "production",
    ):
        assert marker.lower() in combined.lower(), marker


def test_phase11_10_execution_package_remains_discoverable() -> None:
    for path in (
        "docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md",
        "docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md",
        "docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json",
        "tools/phase11_production_equivalent_validation.py",
        "backend/tests/test_phase11_10_production_equivalent_validation.py",
        ".github/workflows/phase11-production-equivalent-validation.yml",
    ):
        assert (ROOT / path).is_file(), path

    combined = "\n".join(_read(path) for path in CURRENT_SURFACES)
    for marker in (
        "historical",
        "fail closed",
        "repository CI",
        "not production authorized",
    ):
        assert marker.lower() in combined.lower(), marker
