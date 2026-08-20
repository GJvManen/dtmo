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
    "docs/architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md",
    "docs/architecture/PHASE11_8D_HA_DISRUPTION.md",
    "docs/architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md",
    "docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md",
    "docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md",
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
    "docs/operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md",
    "docs/operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md",
    "docs/operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md",
    "docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md",
    "docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md",
    "docs/user/THEHIVE_CASE_HANDOFF.md",
    "docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md",
    "docs/administration/KUBERNETES_RUNTIME_CONFIGURATION.md",
    "docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md",
    "docs/administration/INGRESS_TLS_NETWORK_SEGMENTATION.md",
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
    "docs/qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md",
    "docs/qa/PHASE11_8D_HA_DISRUPTION_GATE.md",
    "docs/qa/PHASE11_8E_OBSERVABILITY_GATE.md",
    "docs/qa/PHASE11_8F_RECOVERY_GATE.md",
    "docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md",
    "docs/qa/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md",
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


def _contains_all(path: str, markers: tuple[str, ...], *, casefold: bool = False) -> None:
    text = _read(path)
    haystack = text.lower() if casefold else text
    for marker in markers:
        needle = marker.lower() if casefold else marker
        assert needle in haystack, f"missing {marker!r} from {path}"


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
    _contains_all(
        "README.md",
        (
            "## Why DTMO", "## Product capabilities", "## Architecture",
            "## Current maturity and release position", "## Product roadmap",
            "## Documentation", "## Open source and responsible use",
            "Apache License, Version 2.0", "PostgreSQL", "OpenSearch",
            "Sources & Catalog", "Visual Analytics", "Administration", "Governance",
            "E8.1–E8.10", "Phase 9", "Phase 10", "Phase 11", "Phase 12",
            "Taranis AI", "IntelOwl", "OpenCTI", "MISP", "TheHive",
            "workload identity", "external secret", "ingress/TLS",
        ),
        casefold=True,
    )


def test_architecture_retains_required_layers_and_trust_boundaries() -> None:
    _contains_all(
        "docs/architecture/SYSTEM_ARCHITECTURE.md",
        (
            "## 2. Logical architecture", "### 3.1 Source ingress",
            "### 3.2 Normalization and provenance", "### 3.3 Canonical persistence",
            "### 3.5 Canonical browser product", "### 3.6 Identity and authentication",
            "### 3.7 Authorization and Administration",
            "### 3.10 Governance knowledge and framework mapping",
            "## 4. Trust boundaries", "## 5. Deployment architecture", "## 8. Security invariants",
        ),
    )


def test_current_professional_lifecycle_is_consistent() -> None:
    for path in CURRENT_STATE_DOCUMENTS:
        text = _read(path)
        for marker in (
            "PASS / OWNER_ACCEPTED", "E8", "REPOSITORY_COMPLETE",
            "Phase 9", "EXTERNAL_ASSURANCE_ACCEPTED",
            "Phase 10", "NO-GO / BLOCKED", "Phase 11", "IN PROGRESS",
            "Phase 12", "NOT STARTED",
        ):
            assert marker in text, f"lifecycle marker {marker!r} missing from {path}"
        assert "production" in text.lower()
        for obsolete in OBSOLETE_CURRENT_STATE_MARKERS:
            assert obsolete not in text, f"obsolete lifecycle marker {obsolete!r} remains in {path}"

    _contains_all(
        "docs/project/CURRENT_STATE.md",
        (
            "Phase 11.1–11.2 Taranis | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.3 IntelOwl | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.4 OpenCTI | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.5 MISP | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.6 TheHive | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.7 Cortex decision gate | `PASS / REPOSITORY_COMPLETE — HISTORICAL DECISION BASELINE`",
            "Phase 11.7b Cortex analyzer connector | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8a runtime foundation | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8b workload identity / external secrets | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8c ingress/TLS + network segmentation | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8d HA / disruption hardening | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8e observability hardening | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8f backup / restore / recovery hardening | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8g software supply-chain hardening | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8h capacity / resource planning | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.8i exercised upgrade / rollback | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.9 migration/compatibility | `PASS / REPOSITORY_COMPLETE`",
            "Phase 11.10 production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`",
            "Phase 11.11 independent external assurance | `NOT STARTED`",
            "Phase 12 | `NOT STARTED`",
        ),
    )

    _contains_all(
        "docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md",
        (
            "11.1–11.2 Taranis AI", "11.3 IntelOwl enrichment integration",
            "11.4 OpenCTI knowledge-graph integration", "11.5 MISP consolidation",
            "11.6 TheHive incident/case handoff", "11.7 Cortex decision gate",
            "11.7b Cortex analyzer connector", "11.8 Integrated runtime industrialisation",
            "11.8a Runtime foundation", "11.8b Workload identity and external secret delivery",
            "11.8c Ingress/TLS and network segmentation", "11.8d HA and disruption hardening",
            "11.8e Observability hardening", "11.8f Backup, restore and recovery hardening",
            "11.8g Software supply-chain hardening", "11.8h Capacity and resource planning",
            "11.8i Exercised upgrade and rollback", "11.9 Migration and compatibility",
            "11.10 Integrated production-equivalent validation",
            "**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`",
            "Phase 12 — Production GO/NO-GO",
        ),
    )
    roadmap = _read("docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md")
    assert "#### 11.8i Exercised upgrade and rollback\n**Status:** `PASS / REPOSITORY_COMPLETE`" in roadmap
    assert "### 11.9 Migration and compatibility\n**Status:** `PASS / REPOSITORY_COMPLETE`" in roadmap
    assert "### 11.10 Integrated production-equivalent validation\n**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`" in roadmap


def test_accepted_integration_documents_remain_exposed() -> None:
    _contains_all("docs/architecture/INTELOWL_DTMO_INTEGRATION_CONTRACT.md", ("IntelOwl external Connectors",))
    _contains_all("docs/architecture/OPENCTI_DTMO_INTEGRATION_CONTRACT.md", ("STIX 2.1", "TAXII 2.1", "provenance"))
    _contains_all("docs/architecture/MISP_DTMO_CONSOLIDATION_CONTRACT.md", ("MISP v2.5.44", "AGPL-3.0", "events/restSearch", "events/add", "human"))
    _contains_all("docs/architecture/CORTEX_DTMO_INTEGRATION_CONTRACT.md", ("POST /api/analyzer/{ANALYZER_ID}/run", "responders", "external_share_authorized", "local compromise"))


def test_phase11_runtime_boundaries_remain_professionally_exposed() -> None:
    checks = (
        ("docs/architecture/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md", ("workload identity", "ExternalSecret", "SecretStore", "ClusterSecretStore", "fail closed")),
        ("docs/architecture/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md", ("TLS", "ClusterIP", "namespace selector", "pod selector", "fail closed")),
        ("docs/architecture/PHASE11_8D_HA_DISRUPTION.md", ("availability zone", "anti-affinity", "PodDisruptionBudget", "stateful", "fail closed")),
        ("docs/architecture/PHASE11_8E_OBSERVABILITY_HARDENING.md", ("metrics", "structured", "traces", "fail closed")),
        ("docs/architecture/PHASE11_8F_RECOVERY_HARDENING.md", ("PostgreSQL", "Redis", "OpenSearch", "object storage", "RPO", "RTO", "fail closed")),
        ("docs/security/PHASE11_8G_SUPPLY_CHAIN_HARDENING.md", ("CycloneDX", "vulnerability", "SHA-256", "signed", "provenance", "fail closed")),
    )
    for path, markers in checks:
        _contains_all(path, markers, casefold=True)

    _contains_all("docs/administration/WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md", ("automountServiceAccountToken",))
    _contains_all("docs/administration/INGRESS_TLS_NETWORK_SEGMENTATION.md", ("private key",), casefold=True)
    for path in (
        "docs/operations/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_RUNBOOK.md",
        "docs/operations/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_RUNBOOK.md",
        "docs/operations/PHASE11_8D_HA_DISRUPTION_RUNBOOK.md",
        "docs/operations/PHASE11_8E_OBSERVABILITY_RUNBOOK.md",
        "docs/operations/PHASE11_8G_SUPPLY_CHAIN_RUNBOOK.md",
    ):
        _contains_all(path, ("rollback",), casefold=True)
    _contains_all("docs/operations/PHASE11_8F_RECOVERY_RUNBOOK.md", ("restore", "recovery exercise"), casefold=True)

    for path in (
        "docs/qa/PHASE11_8B_WORKLOAD_IDENTITY_SECRETS_GATE.md",
        "docs/qa/PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION_GATE.md",
        "docs/qa/PHASE11_8D_HA_DISRUPTION_GATE.md",
        "docs/qa/PHASE11_8E_OBSERVABILITY_GATE.md",
        "docs/qa/PHASE11_8F_RECOVERY_GATE.md",
        "docs/qa/PHASE11_8G_SUPPLY_CHAIN_GATE.md",
    ):
        _contains_all(path, ("does not prove",), casefold=True)

    portal = _read("docs/README.md")
    for marker in (
        "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS", "PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION",
        "PHASE11_8D_HA_DISRUPTION", "PHASE11_8E_OBSERVABILITY_HARDENING",
        "PHASE11_8F_RECOVERY_HARDENING", "PHASE11_8G_SUPPLY_CHAIN_HARDENING",
    ):
        assert marker in portal
    evidence = _read("docs/evidence/EVIDENCE_INDEX.md")
    for marker in (
        "phase11-workload-identity-secrets.yml", "phase11-ingress-tls-network.yml",
        "phase11-ha-disruption.yml", "phase11-supply-chain-hardening.yml",
        "release-artifact-attestation.yml",
    ):
        assert marker in evidence


def test_thehive_bounded_implementation_is_exposed_without_false_live_evidence() -> None:
    _contains_all("docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md", ("TheHive 5.5.16", "API v1 (`/api/v1`)", "POST /api/v1/case", "handoff:case"))
    _contains_all("docs/integrations/THEHIVE_HANDOFF.md", ("PASS / REPOSITORY_COMPLETE — ACCEPTED IMPLEMENTATION BASELINE",))
    _contains_all("docs/operations/THEHIVE_HANDOFF_RUNBOOK.md", ("do not blind-retry",), casefold=True)
    _contains_all("docs/user/THEHIVE_CASE_HANDOFF.md", ("ambiguous",))
    _contains_all("docs/administration/THEHIVE_HANDOFF_CONFIGURATION.md", ("DTMO_FEATURE_THEHIVE_HANDOFF",))
    _contains_all("docs/README.md", ("Phase 11.6 TheHive Handoff Implementation Gate",))
    _contains_all("docs/evidence/EVIDENCE_INDEX.md", ("phase11-thehive-handoff-implementation.yml",))


def test_documentation_portal_exposes_guides_and_visual_evidence_boundary() -> None:
    _contains_all(
        "docs/README.md",
        (
            "product/PRODUCT_GUIDE.md", "The governed screenshot catalogue now contains UI-01 through UI-10",
            "documentation illustrations rather than proof of live-source connectivity, staging acceptance or production readiness",
            "CORTEX_ANALYZER_CONNECTOR.md", "PHASE11_7B_CORTEX_CONNECTOR_GATE.md",
            "PHASE11_8_RUNTIME_FOUNDATION.md", "KUBERNETES_RUNTIME_CONFIGURATION.md",
            "PHASE11_8B_WORKLOAD_IDENTITY_SECRETS.md", "WORKLOAD_IDENTITY_EXTERNAL_SECRETS.md",
            "PHASE11_8C_INGRESS_TLS_NETWORK_SEGMENTATION.md", "INGRESS_TLS_NETWORK_SEGMENTATION.md",
            "PHASE11_8D_HA_DISRUPTION.md", "PHASE11_8E_OBSERVABILITY_HARDENING.md",
            "PHASE11_8F_RECOVERY_HARDENING.md", "PHASE11_8G_SUPPLY_CHAIN_HARDENING.md",
            "PHASE11_9_MIGRATION_COMPATIBILITY.md", "PHASE11_9_MIGRATION_COMPATIBILITY_GATE.md",
            "PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_GATE.md",
            "phase11-production-equivalent-validation.yml",
        ),
    )
    _contains_all(
        "docs/evidence/EVIDENCE_INDEX.md",
        (
            "phase11-production-equivalent-validation.yml",
            "test_phase11_10_production_equivalent_validation.py",
            "phase11_production_equivalent_validation.py",
            "candidate identity", "migration/compatibility", "upgrade", "rollback",
            "health", "saturation", "recovery", "fail closed",
        ),
        casefold=True,
    )


def test_stable_professional_documents_do_not_become_operational_run_logs() -> None:
    for path in STABLE_DOCUMENTS:
        text = _read(path)
        for pattern in OPERATIONAL_MARKERS:
            assert pattern.search(text) is None, f"operational chronology marker found in stable document {path}"


def test_documentation_standard_preserves_evidence_separation() -> None:
    _contains_all(
        "docs/project/DOCUMENTATION_STANDARD.md",
        (
            "Class A — stable professional documentation", "Class B — operational and immutable evidence",
            "no PR chronology in project homepage", "architecture is architecture",
            "current phase state must be consistent", "Historical immutable run records",
        ),
        casefold=True,
    )
    _contains_all(
        "docs/project/DOCUMENTATION_STATUS.md",
        ("Authority order", "Current documentation baseline", "Historical / immutable", "Evidence and claim rules"),
        casefold=True,
    )
