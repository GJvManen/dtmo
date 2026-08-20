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

STALE_ACTIVE_MARKERS = (
    "Active bounded priority: Phase 11.8g",
    "active **Phase 11.8g**",
    "active bounded objective is **Phase 11.8g",
    "active bounded step is **Phase 11.8g",
    "active bounded gate is **Phase 11.8g",
    "Phase 11.8g is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "Phase 11.8g supply-chain hardening | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
    "Phase 11.9–11.11 | `NOT STARTED`",
    "Phase 11.10 production-equivalent validation | `NOT STARTED`",
    "Phase 11.10 | New production-equivalent validation | `NOT STARTED`",
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
