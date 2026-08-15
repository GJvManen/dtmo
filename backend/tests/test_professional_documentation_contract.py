from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

STABLE_DOCUMENTS = (
    "README.md",
    "docs/README.md",
    "docs/architecture/SYSTEM_ARCHITECTURE.md",
    "docs/ux/FRONTEND_UX.md",
    "docs/security/SECURITY_OVERVIEW.md",
    "docs/governance/GOVERNANCE_MAPPING_REGISTRY.md",
    "docs/project/CURRENT_STATE.md",
    "docs/project/EXECUTIVE_STATUS.md",
    "docs/project/EXECUTIVE_DECISION_VIEW.md",
    "docs/project/PRODUCTION_READINESS_REPORT.md",
    "docs/project/PRODUCTION_CHECKLIST.md",
    "docs/project/DOCUMENTATION_STATUS.md",
    "docs/evidence/EVIDENCE_INDEX.md",
    "docs/qa/QA_AND_RELEASE_GATES.md",
    "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md",
    "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md",
    "docs/qa/PHASE8_STAGING_READINESS_GATE.md",
    "docs/roadmap/PRODUCTION_ROADMAP.md",
    "docs/releases/16.0.0rc12.md",
)

CURRENT_STATE_DOCUMENTS = (
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
)

OPERATIONAL_MARKERS = (
    re.compile(r"\bPR\s+#\d+\b", re.IGNORECASE),
    re.compile(r"\bRUN-\d{8}-\d+\b"),
    re.compile(r"\b[0-9a-f]{40}\b"),
    re.compile(r"\bworkflow\s+(?:run|job)\s+(?:id\s*)?\d+\b", re.IGNORECASE),
)

OBSOLETE_CURRENT_STATE_MARKERS = (
    "READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY",
    "Phase 8 ready to begin",
    "Real staging is next",
    "E8.8 — governed AIL Project read/enrichment is the active",
    "E8.9–E8.10 not yet accepted",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_professional_documentation_building_blocks_exist() -> None:
    for path in STABLE_DOCUMENTS:
        assert (ROOT / path).is_file(), f"missing professional documentation building block: {path}"

    assert (ROOT / "docs/project/DOCUMENTATION_STANDARD.md").is_file()
    assert (ROOT / "docs/traceability/TRACEABILITY_MATRIX.md").is_file()
    assert (ROOT / "docs/intelligence/SOURCE_CATALOG.md").is_file()
    assert (ROOT / "docs/qa/SOURCE_CONNECTION_MATRIX.md").is_file()


def test_project_readme_retains_professional_product_structure() -> None:
    readme = _read("README.md")
    for heading in (
        "## Why DTMO",
        "## Product capabilities",
        "## Architecture",
        "## Current maturity and release position",
        "## Product roadmap",
        "## Documentation",
        "## Open source and responsible use",
    ):
        assert heading in readme

    for marker in (
        "Apache License, Version 2.0",
        "PostgreSQL",
        "OpenSearch",
        "Sources & Catalog",
        "Visual Analytics",
        "Administration",
        "Governance",
        "E8.1–E8.10",
        "Phase 9",
    ):
        assert marker in readme


def test_architecture_retains_required_layers_and_trust_boundaries() -> None:
    architecture = _read("docs/architecture/SYSTEM_ARCHITECTURE.md")
    for marker in (
        "## 2. Logical architecture",
        "### 3.1 Source ingress",
        "### 3.2 Normalization and provenance",
        "### 3.3 Canonical persistence",
        "### 3.5 Canonical browser product",
        "### 3.6 Identity and authentication",
        "### 3.7 Authorization and Administration",
        "### 3.10 Governance knowledge and framework mapping",
        "## 4. Trust boundaries",
        "## 5. Deployment architecture",
        "## 8. Security invariants",
    ):
        assert marker in architecture


def test_current_professional_lifecycle_is_consistent() -> None:
    for path in CURRENT_STATE_DOCUMENTS:
        text = _read(path)
        assert "PASS / OWNER_ACCEPTED" in text, f"RC13 accepted state missing from {path}"
        assert "E8.1–E8.10" in text, f"E8 completion marker missing from {path}"
        assert "Phase 9" in text, f"Phase 9 marker missing from {path}"
        assert "not production ready" in text.lower() or "production readiness" in text.lower()
        for obsolete in OBSOLETE_CURRENT_STATE_MARKERS:
            assert obsolete not in text, f"obsolete lifecycle marker {obsolete!r} remains in {path}"

    for path in (
        "docs/project/CURRENT_STATE.md",
        "docs/roadmap/PRODUCTION_ROADMAP.md",
    ):
        text = _read(path)
        assert "PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE" in text
        assert "REPOSITORY CONTRACT COMPLETE / EXTERNAL ACCEPTANCE REQUIRED" in text
        assert "Phase 8.5" in text

    current_state = _read("docs/project/CURRENT_STATE.md")
    assert "IN PROGRESS / NEXT" in current_state
    assert "Phase 10" in current_state and "NOT STARTED" in current_state

    phase8_gate = _read("docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md")
    assert "ACTIVE_EXTERNAL_VALIDATION / OWNER_APPROVED_STAGING / IMMUTABLE_EVIDENCE_BINDING_INCOMPLETE" in phase8_gate
    assert "Formal Phase 8 closure still requires that the accepted deployment be bound to one immutable technical identity" in phase8_gate
    assert "Phase 8 is complete only when the immutable staging identity is complete and approved" in phase8_gate
    assert "Repository CI, local Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this gate by themselves" in phase8_gate


def test_stable_professional_documents_do_not_become_operational_run_logs() -> None:
    for path in STABLE_DOCUMENTS:
        text = _read(path)
        for pattern in OPERATIONAL_MARKERS:
            assert pattern.search(text) is None, (
                f"operational chronology marker {pattern.pattern!r} found in stable professional document {path}; "
                "move exact PR/RUN/SHA/workflow history to docs/development or CI evidence"
            )


def test_documentation_standard_preserves_evidence_separation() -> None:
    standard = _read("docs/project/DOCUMENTATION_STANDARD.md")
    for requirement in (
        "Class A — stable professional documentation",
        "Class B — operational and immutable evidence",
        "no PR chronology in project homepage",
        "architecture is architecture",
        "current phase state must be consistent",
        "Historical immutable run records",
    ):
        assert requirement.lower() in standard.lower()

    status = _read("docs/project/DOCUMENTATION_STATUS.md")
    for marker in (
        "Authority order",
        "Current documentation baseline",
        "Historical / immutable",
        "Evidence and claim rules",
    ):
        assert marker.lower() in status.lower()
