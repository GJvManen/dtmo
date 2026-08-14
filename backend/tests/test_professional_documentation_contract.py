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
    "docs/project/PRODUCTION_READINESS_REPORT.md",
    "docs/project/PRODUCTION_CHECKLIST.md",
    "docs/qa/QA_AND_RELEASE_GATES.md",
    "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md",
    "docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md",
    "docs/roadmap/PRODUCTION_ROADMAP.md",
    "docs/releases/16.0.0rc12.md",
)

OPERATIONAL_MARKERS = (
    re.compile(r"\bPR\s+#\d+\b", re.IGNORECASE),
    re.compile(r"\bRUN-\d{8}-\d+\b"),
    re.compile(r"\b[0-9a-f]{40}\b"),
    re.compile(r"\bworkflow\s+(?:run|job)\s+(?:id\s*)?\d+\b", re.IGNORECASE),
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_professional_documentation_building_blocks_exist() -> None:
    for path in STABLE_DOCUMENTS:
        assert (ROOT / path).is_file(), f"missing professional documentation building block: {path}"

    assert (ROOT / "docs/project/DOCUMENTATION_STANDARD.md").is_file()
    assert (ROOT / "docs/evidence/EVIDENCE_INDEX.md").is_file()
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

    assert "Apache License, Version 2.0" in readme
    assert "PostgreSQL" in readme
    assert "OpenSearch" in readme
    assert "Sources & Catalog" in readme
    assert "Visual Analytics" in readme
    assert "Administration" in readme
    assert "Governance" in readme


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
    rc13_docs = (
        "README.md",
        "docs/README.md",
        "docs/project/CURRENT_STATE.md",
        "docs/project/EXECUTIVE_STATUS.md",
        "docs/project/PRODUCTION_READINESS_REPORT.md",
        "docs/project/PRODUCTION_CHECKLIST.md",
        "docs/qa/QA_AND_RELEASE_GATES.md",
        "docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md",
        "docs/roadmap/PRODUCTION_ROADMAP.md",
    )
    for path in rc13_docs:
        text = _read(path)
        assert "PASS / OWNER_ACCEPTED" in text, f"RC13 accepted state missing from {path}"

    # Phase 8.1 has moved from a pending-identity entry condition to an
    # accountable owner-verified external-evidence state. Stable transition
    # documents must reflect that new state while Phase 8 as a whole remains
    # incomplete and proceeds through Phase 8.2-8.5.
    for path in (
        "docs/project/CURRENT_STATE.md",
        "docs/roadmap/PRODUCTION_ROADMAP.md",
    ):
        text = _read(path)
        assert "PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE" in text, (
            f"Phase 8.1 owner-verified state missing from {path}"
        )
        assert "Phase 8.2" in text, f"Phase 8.2 next-state marker missing from {path}"

    current_state = _read("docs/project/CURRENT_STATE.md")
    assert "IN PROGRESS / NEXT" in current_state
    assert "Phase 9" in current_state and "NOT COMPLETE" in current_state
    assert "Phase 10" in current_state and "NOT STARTED" in current_state

    # Older entry/readiness documents may retain the historical pending marker
    # until their dedicated reconciliation, but they must not be used to
    # override the current owner-verified Phase 8.1 state above.
    assert "PENDING_EXTERNAL_DEPLOYMENT_IDENTITY" in _read("docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md")


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
