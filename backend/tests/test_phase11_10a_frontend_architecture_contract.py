from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

ARCHITECTURE = ROOT / "docs/architecture/FRONTEND_ARCHITECTURE.md"
API_CONTRACT = ROOT / "docs/architecture/UI_API_CONTRACT.md"
WORKBENCH = ROOT / "docs/ux/UNIFIED_OPERATIONS_WORKBENCH.md"
INFORMATION_ARCHITECTURE = ROOT / "docs/ux/INFORMATION_ARCHITECTURE.md"
DESIGN_SYSTEM = ROOT / "docs/ux/DESIGN_SYSTEM.md"
QA_GATE = ROOT / "docs/qa/PHASE11_10A_FRONTEND_ARCHITECTURE_GATE.md"
ROADMAP = ROOT / "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md"
CURRENT_STATE = ROOT / "docs/project/CURRENT_STATE.md"
PORTAL = ROOT / "docs/README.md"
EVIDENCE = ROOT / "docs/evidence/EVIDENCE_INDEX.md"
WORKFLOW = ROOT / ".github/workflows/phase11-frontend-architecture.yml"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phase11_10a_required_contract_artifacts_exist() -> None:
    for path in (
        ARCHITECTURE,
        API_CONTRACT,
        WORKBENCH,
        INFORMATION_ARCHITECTURE,
        DESIGN_SYSTEM,
        QA_GATE,
        WORKFLOW,
    ):
        assert path.is_file(), f"missing Phase 11.10a contract artifact: {path.relative_to(ROOT)}"


def test_frontend_architecture_preserves_canonical_trust_path() -> None:
    text = _read(ARCHITECTURE)
    for marker in (
        "React",
        "TypeScript",
        "Vite",
        "TanStack Query",
        "Browser → DTMO API → governed integration adapter → upstream service",
        "server-side RBAC",
        "human/service identity separation",
        "no local-compromise inference",
        "Phase 11.10b implemented the canonical shell",
    ):
        assert marker in text, f"missing frontend architecture marker: {marker}"


def test_ui_api_contract_is_governed_and_fail_closed() -> None:
    text = _read(API_CONTRACT)
    for marker in (
        "DTMO browser → DTMO `/api/v1/...` → authorization/audit",
        "must not directly invoke Taranis AI, IntelOwl, OpenCTI, MISP, TheHive or Cortex",
        "server-authorized",
        "case handoff/case mutation",
        "external share/publication approval",
        "prepare → review → explicit share approval → publish/synchronize when authorized",
        "No enrichment result alone proves local compromise",
    ):
        assert marker in text, f"missing governed UI/API marker: {marker}"


def test_information_architecture_exposes_full_workbench_domains() -> None:
    text = _read(INFORMATION_ARCHITECTURE)
    for marker in (
        "Command Center",
        "Threat Intelligence",
        "Exposure",
        "Investigations",
        "Analysis",
        "Sharing",
        "Automation",
        "Collection",
        "Governance",
        "Operations",
        "Administration",
        "Context rail contract",
    ):
        assert marker in text, f"missing information architecture domain: {marker}"


def test_design_system_preserves_accessibility_and_truthful_state() -> None:
    text = _read(DESIGN_SYSTEM)
    for marker in (
        "dark operations mode",
        "light mode",
        "informational",
        "low",
        "medium",
        "high",
        "critical",
        "Colour is supplementary",
        "partial failure",
        "WCAG 2.2 AA",
        "Mockups, generated visuals and design-system examples are design artifacts only",
    ):
        assert marker in text, f"missing design-system marker: {marker}"


def test_workbench_defines_candidate_completion_sequence() -> None:
    text = _read(WORKBENCH)
    for marker in (
        "Collect → Normalize → Enrich → Correlate → Investigate → Respond → Share → Learn",
        "11.10a frontend architecture/design contract — `PASS / REPOSITORY_COMPLETE`",
        "11.10b canonical application shell — `PASS / REPOSITORY_COMPLETE`",
        "11.10c Command Center — `PASS / REPOSITORY_COMPLETE`",
        "11.10d Unified Intelligence Workspace — active",
        "11.10o consolidation/full functional acceptance",
        "11.10p fresh production-equivalent exercise",
        "Phase 11.11 remains blocked until 11.10p is explicitly accepted",
    ):
        assert marker in text, f"missing workbench sequencing marker: {marker}"


def test_authoritative_surfaces_preserve_accepted_architecture_and_current_slice() -> None:
    for path in (ROADMAP, CURRENT_STATE, PORTAL, EVIDENCE):
        text = _read(path)
        assert "Phase 11.10" in text
        assert "11.10a" in text, f"11.10a is not exposed in {path.relative_to(ROOT)}"
        assert "11.10b" in text, f"11.10b is not exposed in {path.relative_to(ROOT)}"
        assert "11.10c" in text, f"11.10c is not exposed in {path.relative_to(ROOT)}"
        assert "11.10d" in text, f"11.10d is not exposed in {path.relative_to(ROOT)}"
        assert "not production authorized" in text.lower() or "does not authorize production" in text.lower() or "production authorization" in text.lower()

    current = _read(CURRENT_STATE)
    assert "Phase 11.10a frontend architecture/design contract | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10b canonical application shell | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10c Command Center | `PASS / REPOSITORY_COMPLETE`" in current
    assert "Phase 11.10d Unified Intelligence Workspace | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`" in current
    assert "Phase 11.10e IntelOwl/Cortex integrated analysis | `NOT STARTED`" in current

    roadmap = _read(ROADMAP)
    assert "11.10a Frontend architecture and design contract" in roadmap
    assert "11.10b Canonical application shell" in roadmap
    assert "11.10c Command Center" in roadmap
    assert "11.10d Unified Intelligence Workspace" in roadmap
    assert "11.10p Fresh production-equivalent validation" in roadmap


def test_phase11_10a_gate_preserves_repository_evidence_boundary() -> None:
    text = _read(QA_GATE)
    for marker in (
        "repository contract consistency only",
        "does not accept the new shell",
        "does not accept",
        "production-equivalent",
        "Phase 11.10b — canonical application shell",
    ):
        assert marker in text
