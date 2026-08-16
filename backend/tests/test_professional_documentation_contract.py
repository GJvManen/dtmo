from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

STABLE_DOCUMENTS = (
    "README.md",
    "docs/README.md",
    "docs/architecture/SYSTEM_ARCHITECTURE.md",
    "docs/architecture/TARANIS_PLATFORM_INTEGRATION_ASSESSMENT.md",
    "docs/architecture/TARANIS_DTMO_INTEGRATION_CONTRACT.md",
    "docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md",
    "docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md",
    "docs/integrations/TARANIS_ADAPTER.md",
    "docs/integrations/INTELOWL_INTEGRATION.md",
    "docs/integrations/OPENCTI_INTEGRATION.md",
    "docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md",
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
    "docs/qa/PHASE11_4_OPENCTI_CONTRACT_GATE.md",
    "docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md",
    "docs/roadmap/PRODUCTION_ROADMAP.md",
    "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md",
    "docs/production/PHASE10_PRODUCTION_GO_NO_GO.md",
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
    "docs/production/PHASE10_PRODUCTION_GO_NO_GO.md",
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
    "Phase 9 `NOT COMPLETE`",
    "Phase 10 `NOT STARTED`",
    "Phase 10 `IN PROGRESS / DECISION REQUIRED`",
    "IN PROGRESS / ACCOUNTABLE PRODUCTION DECISION REQUIRED",
)


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_professional_documentation_building_blocks_exist() -> None:
    for path in STABLE_DOCUMENTS:
        assert (ROOT / path).is_file(), f"missing professional documentation building block: {path}"
    for path in (
        "docs/project/DOCUMENTATION_STANDARD.md",
        "docs/traceability/TRACEABILITY_MATRIX.md",
        "docs/intelligence/SOURCE_CATALOG.md",
        "docs/qa/SOURCE_CONNECTION_MATRIX.md",
    ):
        assert (ROOT / path).is_file()


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
        "Phase 10",
        "Phase 11",
        "Phase 12",
        "Taranis AI",
        "IntelOwl",
        "OpenCTI",
        "TheHive",
        "Phase 11.3 IntelOwl",
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

    opencti = _read("docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md")
    for marker in ("7.260811.0", "service-to-service", "STIX 2.1", "TAXII 2.1", "provenance", "Apache-2.0", "Enterprise Edition"):
        assert marker in opencti


def test_current_professional_lifecycle_is_consistent() -> None:
    for path in CURRENT_STATE_DOCUMENTS:
        text = _read(path)
        assert "PASS / OWNER_ACCEPTED" in text, f"accountable acceptance state missing from {path}"
        assert "E8" in text and "REPOSITORY_COMPLETE" in text, f"E8 repository completion missing from {path}"
        assert "Phase 9" in text and "EXTERNAL_ASSURANCE_ACCEPTED" in text, f"Phase 9 acceptance missing from {path}"
        assert "Phase 10" in text and "NO-GO / BLOCKED" in text, f"Phase 10 no-go missing from {path}"
        assert "Phase 11" in text and "IN PROGRESS" in text, f"active Phase 11 state missing from {path}"
        assert "Phase 12" in text and "NOT STARTED" in text, f"Phase 12 state missing from {path}"
        assert "production" in text.lower()
        for obsolete in OBSOLETE_CURRENT_STATE_MARKERS:
            assert obsolete not in text, f"obsolete lifecycle marker {obsolete!r} remains in {path}"

    current_state = _read("docs/project/CURRENT_STATE.md")
    for marker in (
        "Phase 11.2 Taranis adapter | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.3 IntelOwl contract | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.3 IntelOwl adapter | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.3 governed execution/persistence | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.4 OpenCTI contract | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.4 OpenCTI read-only adapter | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.4 OpenCTI canonical mapping/persistence | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 12 | `NOT STARTED`",
    ):
        assert marker in current_state

    industrialisation = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    assert "11.2 Taranis → DTMO canonical adapter\n\n**Status:** `PASS / REPOSITORY_COMPLETE`" in industrialisation
    assert "11.3 IntelOwl enrichment integration\n\n**Status:** `PASS / REPOSITORY_COMPLETE`" in industrialisation
    assert "11.4 OpenCTI knowledge-graph integration\n\n**Status:** `IN PROGRESS / CANONICAL PERSISTENCE IN EXACT-HEAD VALIDATION`" in industrialisation
    assert "11.5 MISP consolidation" in industrialisation
    assert "11.6 TheHive incident/case handoff" in industrialisation
    assert "11.7 Cortex decision gate" in industrialisation
    assert "Phase 12 — Production GO/NO-GO" in industrialisation


def test_intelowl_contract_and_integration_docs_are_synchronized() -> None:
    assert "IntelOwl external Connectors" in _read("docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md")
    assert "IntelOwl external Connectors" in _read("docs/integrations/INTELOWL_INTEGRATION.md")
    assert "IntelOwl → DTMO Integration Contract" in _read("docs/README.md")
    assert "Phase 11 IntelOwl Integration Contract Gate" in _read("docs/qa/QA_AND_RELEASE_GATES.md")
    assert "phase11-intelowl-integration-contract.yml" in _read("docs/evidence/EVIDENCE_INDEX.md")


def test_opencti_documents_are_synchronized_with_persistence_slice() -> None:
    contract = _read("docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md")
    integration = _read("docs/integrations/OPENCTI_INTEGRATION.md")
    runbook = _read("docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md")
    portal = _read("docs/README.md")
    evidence = _read("docs/evidence/EVIDENCE_INDEX.md")
    gate = _read("docs/qa/PHASE11_4_OPENCTI_PERSISTENCE_GATE.md")

    for marker in ("STIX 2.1", "TAXII 2.1", "provenance"):
        assert marker in contract
    for marker in ("opencti_object_mappings", "opencti_mapping_revisions", "commit_page(page)", "provenance"):
        assert marker in integration
    for marker in ("0012_opencti_mapping_persistence", "PostgreSQL commit", "idempotent"):
        assert marker in runbook
    assert "Phase 11.4 OpenCTI persistence" in portal
    assert "backend/tests/test_phase11_4_opencti_persistence.py" in evidence
    assert "external_share_authorized=false" in gate
    assert "phase11-opencti-integration-contract.yml" in evidence


def test_documentation_portal_exposes_audience_guides_and_visual_evidence_boundary() -> None:
    portal = _read("docs/README.md")
    assert "product/PRODUCT_GUIDE.md" in portal
    assert "The governed screenshot catalogue now contains UI-01 through UI-10" in portal
    assert "documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness" in portal


def test_stable_professional_documents_do_not_become_operational_run_logs() -> None:
    for path in STABLE_DOCUMENTS:
        text = _read(path)
        for pattern in OPERATIONAL_MARKERS:
            assert pattern.search(text) is None, f"operational chronology marker found in stable document {path}"


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
    for marker in ("Authority order", "Current documentation baseline", "Historical / immutable", "Evidence and claim rules"):
        assert marker.lower() in status.lower()
