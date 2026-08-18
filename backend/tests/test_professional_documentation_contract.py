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
    "docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md",
    "docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md",
    "docs/architecture/CORTEX_DECISION_GATE.md",
    "docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md",
    "docs/architecture/PHASE11_8_RUNTIME_FOUNDATION.md",
    "docs/architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md",
    "docs/integrations/TARANIS_ADAPTER.md",
    "docs/integrations/INTELOWL_INTEGRATION.md",
    "docs/integrations/OPENCTI_INTEGRATION.md",
    "docs/integrations/THEHIVE_HANDOFF.md",
    "docs/integrations/CORTEX_ANALYZER_CONNECTOR.md",
    "docs/operations/OPENCTI_INTEGRATION_RUNBOOK.md",
    "docs/operations/THEHIVE_HANDOFF_RUNBOOK.md",
    "docs/operations/CORTEX_ANALYZER_RUNBOOK.md",
    "docs/operations/PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md",
    "docs/operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md",
    "docs/user/THEHIVE_CASE_HANDOFF.md",
    "docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md",
    "docs/administration/KUBERNETES_RUNTIME_CONFIGURATION.md",
    "docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md",
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
    "docs/qa/PHASE11_5_MISP_CONSOLIDATION_CONTRACT_GATE.md",
    "docs/qa/PHASE11_5_MISP_CONSOLIDATION_STATE_GATE.md",
    "docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md",
    "docs/qa/PHASE11_6_THEHIVE_HANDOFF_IMPLEMENTATION_GATE.md",
    "docs/qa/PHASE11_7_CORTEX_DECISION_GATE.md",
    "docs/qa/PHASE11_7B_CORTEX_CONNECTOR_GATE.md",
    "docs/qa/PHASE11_8_RUNTIME_FOUNDATION_GATE.md",
    "docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md",
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
    "BOUNDED HANDOFF IMPLEMENTATION IN EXACT-HEAD VALIDATION",
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
        "## Why DTMO", "## Product capabilities", "## Architecture",
        "## Current maturity and release position", "## Product roadmap",
        "## Documentation", "## Open source and responsible use",
    ):
        assert heading in readme
    for marker in (
        "Apache License, Version 2.0", "PostgreSQL", "OpenSearch", "Sources & Catalog",
        "Visual Analytics", "Administration", "Governance", "E8.1–E8.10", "Phase 9",
        "Phase 10", "Phase 11", "Phase 12", "Taranis AI", "IntelOwl", "OpenCTI",
        "MISP", "TheHive", "workload identity", "external secret",
    ):
        assert marker.lower() in readme.lower()


def test_architecture_retains_required_layers_and_trust_boundaries() -> None:
    architecture = _read("docs/architecture/SYSTEM_ARCHITECTURE.md")
    for marker in (
        "## 2. Logical architecture", "### 3.1 Source ingress",
        "### 3.2 Normalization and provenance", "### 3.3 Canonical persistence",
        "### 3.5 Canonical browser product", "### 3.6 Identity and authentication",
        "### 3.7 Authorization and Administration", "### 3.10 Governance knowledge and framework mapping",
        "## 4. Trust boundaries", "## 5. Deployment architecture", "## 8. Security invariants",
    ):
        assert marker in architecture


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
        "Phase 11.1–11.2 Taranis | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.3 IntelOwl | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.4 OpenCTI | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.7 Cortex decision gate | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`",
        "Phase 11.7b Cortex analyzer connector | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.8a runtime foundation | `PASS / REPOSITORY_COMPLETE`",
        "Phase 11.8b workload identity / external secrets | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 11.9 migration/compatibility | `NOT STARTED`",
        "Phase 11.10 production-equivalent validation | `NOT STARTED`",
        "Phase 11.11 independent external assurance | `NOT STARTED`",
        "Phase 12 | `NOT STARTED`",
    ):
        assert marker in current_state

    industrialisation = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    for marker in (
        "11.1–11.2 Taranis AI\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.3 IntelOwl enrichment integration\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.4 OpenCTI knowledge-graph integration\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.5 MISP consolidation\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.6 TheHive incident/case handoff\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.7 Cortex decision gate\n\n**Status:** `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`",
        "11.7b Cortex analyzer connector\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.8 Integrated runtime industrialisation",
        "11.8a Runtime foundation\n\n**Status:** `PASS / REPOSITORY_COMPLETE`",
        "11.8b Workload identity and external secret delivery\n\n**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`",
        "Phase 12 — Production GO/NO-GO",
    ):
        assert marker in industrialisation


def test_accepted_integration_documents_remain_exposed() -> None:
    assert "IntelOwl external Connectors" in _read("docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md")
    for marker in ("STIX 2.1", "TAXII 2.1", "provenance"):
        assert marker in _read("docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md")
    for marker in ("MISP v2.5.44", "AGPL-3.0", "events/restSearch", "events/add", "human"):
        assert marker in _read("docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md")
    for marker in ("POST /api/analyzer/{ANALYZER_ID}/run", "responders", "external_share_authorized", "local compromise"):
        assert marker in _read("docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md")


def test_phase11_8b_secret_identity_boundary_is_professionally_exposed() -> None:
    architecture = _read("docs/architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md")
    admin = _read("docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md")
    runbook = _read("docs/operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md")
    gate = _read("docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md")
    portal = _read("docs/README.md")
    evidence = _read("docs/evidence/EVIDENCE_INDEX.md")
    for marker in ("workload identity", "ExternalSecret", "SecretStore", "ClusterSecretStore", "fail closed"):
        assert marker.lower() in architecture.lower()
    assert "automountServiceAccountToken" in admin
    assert "rollback" in runbook.lower()
    assert "does not prove" in gate.lower()
    assert "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS" in portal
    assert "phase11-workload-identity-secrets.yml" in evidence


def test_thehive_bounded_implementation_is_exposed_without_false_live_evidence() -> None:
    contract = _read("docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md")
    for marker in ("TheHive 5.5.16", "API v1 (`/api/v1`)", "POST /api/v1/case", "handoff:case"):
        assert marker in contract
    assert "PASS / REPOSITORY_COMPLETE — ACCEPTED IMPLEMENTATION BASELINE" in _read("docs/integrations/THEHIVE_HANDOFF.md")
    assert "do not blind-retry" in _read("docs/operations/THEHIVE_HANDOFF_RUNBOOK.md").lower()
    assert "ambiguous" in _read("docs/user/THEHIVE_CASE_HANDOFF.md")
    assert "DTMO_FEATURE_THEHIVE_HANDOFF" in _read("docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md")
    assert "Phase 11.6 TheHive Handoff Implementation Gate" in _read("docs/README.md")
    assert "phase11-thehive-handoff-implementation.yml" in _read("docs/evidence/EVIDENCE_INDEX.md")


def test_documentation_portal_exposes_audience_guides_and_visual_evidence_boundary() -> None:
    portal = _read("docs/README.md")
    for marker in (
        "product/PRODUCT_GUIDE.md", "The governed screenshot catalogue now contains UI-01 through UI-10",
        "documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness",
        "CORTEX_ANALYZER_CONNECTOR.md", "PHASE11_7B_CORTEX_CONNECTOR_GATE.md",
        "PHASE11_8_RUNTIME_FOUNDATION.md", "KUBERNETES_RUNTIME_CONFIGURATION.md",
        "PHASE11_8_RUNTIME_FOUNDATION_RUNBOOK.md", "PHASE11_8_RUNTIME_FOUNDATION_GATE.md",
        "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md", "WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md",
        "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md", "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md",
    ):
        assert marker in portal


def test_stable_professional_documents_do_not_become_operational_run_logs() -> None:
    for path in STABLE_DOCUMENTS:
        text = _read(path)
        for pattern in OPERATIONAL_MARKERS:
            assert pattern.search(text) is None, f"operational chronology marker found in stable document {path}"


def test_documentation_standard_preserves_evidence_separation() -> None:
    standard = _read("docs/project/DOCUMENTATION_STANDARD.md")
    for requirement in (
        "Class A — stable professional documentation", "Class B — operational and immutable evidence",
        "no PR chronology in project homepage", "architecture is architecture",
        "current phase state must be consistent", "Historical immutable run records",
    ):
        assert requirement.lower() in standard.lower()
    status = _read("docs/project/DOCUMENTATION_STATUS.md")
    for marker in ("Authority order", "Current documentation baseline", "Historical / immutable", "Evidence and claim rules"):
        assert marker.lower() in status.lower()
