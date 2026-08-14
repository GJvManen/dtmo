from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])

_EVIDENCE_MAPPINGS: tuple[dict[str, object], ...] = (
    {
        "evidence_id": "E8-VULN-INGEST",
        "title": "Provenance-preserved vulnerability intelligence",
        "normenkader": ["SM.07"],
        "evidence_refs": ["backend/dtmo/connectors/opencve.py", "backend/dtmo/connectors/vulnerability_lookup.py"],
        "semantics": ["CVE", "CWE", "vendor/product/CPE", "source provenance"],
        "boundary": "Source intelligence supports threat and vulnerability assessment; it does not prove local deployment, exposure, exploitability or compromise.",
    },
    {
        "evidence_id": "E8-VULN-PRIORITY",
        "title": "Explainable vulnerability prioritization",
        "normenkader": ["SM.07"],
        "evidence_refs": ["backend/dtmo/vulnerability_prioritization.py", "backend/dtmo/vulnerability_relevance.py"],
        "semantics": ["CVSS severity", "EPSS probability", "KEV exploitation context", "sightings", "governed relevance"],
        "boundary": "Priority is an operational triage aid, not an organizational risk score or remediation authority.",
    },
    {
        "evidence_id": "E8-VULN-ANALYTICS",
        "title": "Governed vulnerability analytics and provenance",
        "normenkader": ["SM.07", "SM.04"],
        "evidence_refs": ["backend/dtmo/vulnerability_analytics.py", "backend/dtmo/vulnerability_console.py"],
        "semantics": ["24h/7d/30d trends", "filters", "raw SHA-256 provenance", "degraded evidence state"],
        "boundary": "Analytics summarizes available evidence and preserves missing/degraded states; it does not certify completeness.",
    },
    {
        "evidence_id": "E8-MISP-GOVERNANCE",
        "title": "MISP restriction-aware CTI exchange",
        "normenkader": ["SM.07", "SM.04"],
        "evidence_refs": ["backend/dtmo/connectors/misp.py", "backend/dtmo/misp_export.py"],
        "semantics": ["MISP taxonomy/galaxy", "TLP", "distribution", "sharing group", "separate share approval"],
        "boundary": "MISP taxonomy classifies CTI while TLP/distribution constrain sharing; neither is a vulnerability severity or risk score.",
    },
    {
        "evidence_id": "E8-AIL-CONTEXT",
        "title": "Data-minimized AIL investigation context",
        "normenkader": ["SM.07"],
        "evidence_refs": ["backend/dtmo/connectors/ail.py", "backend/dtmo/ail_correlation.py"],
        "semantics": ["allowlisted extracted indicators", "exact correlation", "bounded investigation identifiers"],
        "boundary": "AIL context is investigative source evidence; raw leak content is excluded and correlation does not infer compromise or attribution.",
    },
    {
        "evidence_id": "E8-ATTACK-CONTEXT",
        "title": "MITRE ATT&CK behavioral classification context",
        "normenkader": ["SM.07"],
        "evidence_refs": ["backend/dtmo/framework_governance.py"],
        "semantics": ["ATT&CK technique identifiers", "human-reviewed explicit mappings"],
        "boundary": "ATT&CK describes adversary behavior and detection context; it is not control equivalence, vulnerability severity or proof of observed behavior.",
    },
)


def vulnerability_evidence_mapping() -> dict[str, object]:
    return {
        "status": "repository_backed_explicit_evidence_mapping",
        "verified_on": "2026-08-14",
        "primary_control": "SM.07",
        "supporting_controls": ["SM.04"],
        "mappings": [dict(item) for item in _EVIDENCE_MAPPINGS],
        "semantic_boundaries": {
            "CVSS": "vulnerability severity",
            "EPSS": "probability of exploitation in the wild",
            "KEV": "known-exploited vulnerability catalog context",
            "MITRE ATT&CK": "adversary behavior classification",
            "MISP taxonomy/TLP/distribution": "CTI classification and sharing constraints",
            "AIL": "data-minimized investigative and extracted-indicator context",
        },
        "claim_boundary": (
            "This mapping identifies repository evidence that supports Normenkader IBP threat- and vulnerability-management activities. "
            "It is not a compliance, maturity, certification, exposure, compromise, remediation-completion or external-acceptance claim."
        ),
    }


@router.get("/vulnerability-evidence-mapping")
def governance_vulnerability_evidence_mapping(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
) -> dict[str, object]:
    del principal
    return vulnerability_evidence_mapping()
