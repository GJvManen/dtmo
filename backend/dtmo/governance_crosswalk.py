from __future__ import annotations

from typing import Annotated, cast

from fastapi import APIRouter, Depends

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])

# This crosswalk maps concrete DTMO controls/capabilities to external framework
# objects. Relationships are deliberately typed and never claim certification or
# full framework compliance. Sources are authoritative framework-owner pages.
_CONTROL_CROSSWALK: tuple[dict[str, object], ...] = (
    {
        "dtmo_control_id": "DTMO-IAM-01",
        "title": "Governed RBAC and least privilege",
        "implementation_refs": [
            "backend/dtmo/rbac_admin.py",
            "backend/dtmo/rbac_management_experience.py",
            "docs/security/SECURITY_OVERVIEW.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "ID.02",
                "object_title": "Administratie van toegangsrechten",
                "relationship": "supports",
                "rationale": "DTMO beheert toegang via rollen, least privilege en gecontroleerde toekenning van rechten.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-10-identity-en-accessmanagement/id-02-administratie-van-toegangsrechten/",
            },
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "ID.05",
                "object_title": "Periodieke beoordeling van toegangsrechten",
                "relationship": "supports",
                "rationale": "De Administration-laag maakt actuele principal-, rol- en permissiontoekenningen expliciet en auditeerbaar.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-10-identity-en-accessmanagement/id-05-periodieke-beoordeling-van-toegangsrechten/",
            },
            {
                "framework_id": "nist-csf",
                "object_type": "category",
                "object_id": "PR.AA",
                "object_title": "Identity Management, Authentication, and Access Control",
                "relationship": "supports",
                "rationale": "DTMO RBAC, authentication boundaries and least-privilege administration support access-control outcomes.",
                "source_url": "https://www.nist.gov/cyberframework",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-AUTH-01",
        "title": "Authenticated and attributable access",
        "implementation_refs": [
            "backend/dtmo/auth/",
            "docs/security/SECURITY_OVERVIEW.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "SM.02",
                "object_title": "Authenticatiemechanismes",
                "relationship": "supports",
                "rationale": "DTMO koppelt beschermde functies aan geauthenticeerde principals en server-side autorisatie.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-11-securitymanagement/sm-02-authenticatiemechanismes/",
            },
            {
                "framework_id": "mitre-attack",
                "object_type": "technique",
                "object_id": "T1078",
                "object_title": "Valid Accounts",
                "relationship": "detection-and-mitigation-context",
                "rationale": "Identity telemetry, revocation and least privilege are relevant controls for detecting and limiting abuse of valid accounts; this is not a technique-equivalence claim.",
                "source_url": "https://attack.mitre.org/techniques/T1078/",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-AUD-01",
        "title": "Tamper-evident audit and request correlation",
        "implementation_refs": [
            "backend/dtmo/audit/",
            "backend/dtmo/trace_context.py",
            "docs/security/SECURITY_OVERVIEW.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "SM.04",
                "object_title": "Logging systeemactiviteiten",
                "relationship": "supports",
                "rationale": "DTMO registreert beveiligingsrelevante acties met actor, resource, decision en request/correlation context.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-11-securitymanagement/sm-04-logging-systeemactiviteiten/",
            },
            {
                "framework_id": "nist-csf",
                "object_type": "category",
                "object_id": "DE.CM",
                "object_title": "Continuous Monitoring",
                "relationship": "supports",
                "rationale": "Audit, logging, metrics and alerting provide observable evidence used by monitoring and detection processes.",
                "source_url": "https://www.nist.gov/cyberframework",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-TVM-01",
        "title": "Threat and vulnerability intelligence lifecycle",
        "implementation_refs": [
            "backend/dtmo/connectors/",
            "backend/dtmo/api/routes.py",
            "docs/intelligence/SOURCE_CATALOG.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "SM.07",
                "object_title": "Threat- en vulnerabilitymanagement",
                "relationship": "supports",
                "rationale": "DTMO verzamelt, normaliseert en bewaart provenance voor threat- en vulnerability intelligence ten behoeve van beoordeling en opvolging.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-11-securitymanagement/sm-07-threat-en-vulnerabilitymanagement/",
            },
            {
                "framework_id": "mitre-attack",
                "object_type": "technique",
                "object_id": "T1087",
                "object_title": "Account Discovery",
                "relationship": "threat-classification-context",
                "rationale": "ATT&CK technique identifiers provide explicit behavioral context for intelligence records when reviewed and mapped; DTMO does not infer this technique from free text.",
                "source_url": "https://attack.mitre.org/techniques/T1087/",
            },
            {
                "framework_id": "nist-csf",
                "object_type": "category",
                "object_id": "ID.RA",
                "object_title": "Risk Assessment",
                "relationship": "supports",
                "rationale": "Traceable threat and vulnerability intelligence supplies evidence used to understand cybersecurity risk.",
                "source_url": "https://www.nist.gov/cyberframework",
            },
            {
                "framework_id": "cvss",
                "object_type": "scoring_context",
                "object_id": "CVSS:4.0",
                "object_title": "Common Vulnerability Scoring System v4.0",
                "relationship": "context-only",
                "rationale": "CVSS may contextualize vulnerability severity, but DTMO still does not claim a first-class vector/base-score contract.",
                "source_url": "https://www.first.org/cvss/v4.0/specification-document",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-NET-01",
        "title": "Network and deployment trust boundaries",
        "implementation_refs": [
            "infrastructure/gateway/nginx.conf",
            "docs/architecture/SYSTEM_ARCHITECTURE.md",
            "docs/security/SECURITY_OVERVIEW.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "SM.11",
                "object_title": "Netwerkbeveiliging",
                "relationship": "supports",
                "rationale": "DTMO documenteert trust boundaries, gateway controls and production requirements for TLS, network controls and least-privilege service access.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-11-securitymanagement/sm-11-netwerkbeveiliging/",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-REC-01",
        "title": "Backup, restore and recovery evidence",
        "implementation_refs": [
            "docs/operations/OPERATIONS_MANUAL.md",
            "docs/project/PRODUCTION_CHECKLIST.md",
            ".github/workflows/rc6-multistore-recovery.yml",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "OP.02",
                "object_title": "Procedures voor back-up en herstel",
                "relationship": "supports",
                "rationale": "DTMO release gates exercise backup/restore integrity and require environment-specific recovery evidence for production readiness.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-13-it-operatie/op-02-procedures-voor-back-up-en-herstel/",
            },
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "BC.03",
                "object_title": "Offsite back-upopslag",
                "relationship": "partial-support",
                "rationale": "Repository recovery controls support restore assurance; offsite production storage remains environment-specific and is not claimed by local CI.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-14-bedrijfscontinuiteitsmanagement/bc-03-offsite-back-upopslag/",
            },
            {
                "framework_id": "nist-csf",
                "object_type": "category",
                "object_id": "RC.RP",
                "object_title": "Incident Recovery Plan Execution",
                "relationship": "supports",
                "rationale": "Recovery runbooks and restore evidence support controlled restoration, while production recovery acceptance remains an environment gate.",
                "source_url": "https://www.nist.gov/cyberframework",
            },
        ],
    },
    {
        "dtmo_control_id": "DTMO-GOV-01",
        "title": "Evidence-based release governance",
        "implementation_refs": [
            "docs/project/PROJECT_GOVERNANCE.md",
            "docs/qa/QA_AND_RELEASE_GATES.md",
            "docs/roadmap/PRODUCTION_ROADMAP.md",
        ],
        "mappings": [
            {
                "framework_id": "normenkader-ibp",
                "object_type": "control",
                "object_id": "GO.03",
                "object_title": "Planning/roadmap informatiebeveiliging",
                "relationship": "supports",
                "rationale": "DTMO maintains an evidence-driven security roadmap with explicit release/readiness phases and accountable decision boundaries.",
                "source_url": "https://normenkaderibp.kennisnet.nl/informatiebeveiliging/domein-1-bestuur/go-03-planningroadmap-informatiebeveiliging/",
            },
            {
                "framework_id": "nist-csf",
                "object_type": "function",
                "object_id": "GV",
                "object_title": "Govern",
                "relationship": "supports",
                "rationale": "Project governance, risk, assurance and accountable go/no-go structures support cybersecurity governance outcomes.",
                "source_url": "https://www.nist.gov/cyberframework",
            },
        ],
    },
)


def control_crosswalk() -> dict[str, object]:
    mappings = [
        mapping
        for control in _CONTROL_CROSSWALK
        for mapping in cast(list[dict[str, object]], control["mappings"])
    ]
    by_framework: dict[str, int] = {}
    for mapping in mappings:
        framework_id = str(mapping["framework_id"])
        by_framework[framework_id] = by_framework.get(framework_id, 0) + 1
    return {
        "status": "repository_backed_explicit_partial_crosswalk",
        "verified_on": "2026-08-14",
        "controls": [dict(control) for control in _CONTROL_CROSSWALK],
        "mapping_count": len(mappings),
        "mapping_count_by_framework": by_framework,
        "claim_boundary": (
            "Mappings are explicit typed relationships between DTMO capabilities and framework objects. "
            "They do not constitute certification, full compliance, or semantic equivalence. "
            "Environment-dependent controls remain partial until environment evidence exists."
        ),
    }


@router.get("/control-crosswalk")
def governance_control_crosswalk(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
) -> dict[str, object]:
    del principal
    return control_crosswalk()
