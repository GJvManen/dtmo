from __future__ import annotations

from typing import Annotated, cast

from fastapi import APIRouter, Depends

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal
from dtmo.governance_crosswalk import control_crosswalk

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])

_INTERNAL_MAPPINGS: tuple[dict[str, object], ...] = (
    {"id": "identity-access", "title": "Identity & access control", "statement": "RBAC en least privilege zijn verplicht; service accounts krijgen geen human review/share authority.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Identity and access control"},
    {"id": "separation-of-duties", "title": "Separation of duties", "statement": "Technische toegang, deployment, CI of operations impliceert geen publication/share approval.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Separation of duties"},
    {"id": "privacy-provenance", "title": "Privacy, provenance & confidence", "statement": "Dataminimalisatie, bronprovenance en confidence moeten behouden blijven; secrets horen niet in repository of evidence.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Data protection and privacy"},
    {"id": "exact-head-evidence", "title": "Exact-head release evidence", "statement": "Een PASS-claim vereist uitvoerbare exact-head evidence; workflowdefinitie alleen is onvoldoende.", "source": "docs/traceability/TRACEABILITY_MATRIX.md", "section": "Traceability rule"},
    {"id": "external-assurance-boundary", "title": "External assurance boundary", "statement": "Repository emulator/runtime evidence bewijst geen real staging, pentest of production acceptance.", "source": "docs/traceability/TRACEABILITY_MATRIX.md", "section": "Phase 8/9/10 rows"},
    {"id": "threat-vulnerability-management", "title": "Threat & vulnerability management", "statement": "CVE/vendor advisory beoordeling moet doelgebonden zijn en provenance, tijd, applicability en confidence vastleggen.", "source": "docs/security/SECURITY_OVERVIEW.md", "section": "Threat and vulnerability management"},
)

_AUTHORITY_BOUNDARIES: tuple[str, ...] = (
    "Dashboard- of consolezichtbaarheid verleent geen publication/share authority.",
    "Human review en externe share approval blijven afzonderlijke bevoegdheden.",
    "Service accounts/connectors krijgen geen human approval powers.",
    "Ontbrekende, stale, inferred of inaccessible evidence telt niet als PASS.",
    "Frameworkrelaties bewijzen geen certificering, volledige compliance of operationele effectiviteit.",
    "Repository CI is geen production-equivalent validation, independent assurance of production authorization.",
)

_FRAMEWORK_META: tuple[dict[str, str], ...] = (
    {"id": "normenkader-ibp", "name": "Normenkader IBP", "kind": "education-security-framework", "coverage_label": "Expliciete partiële crosswalk"},
    {"id": "mitre-attack", "name": "MITRE ATT&CK", "kind": "threat-behavior-taxonomy", "coverage_label": "Expliciete contextrelaties"},
    {"id": "nist-csf", "name": "NIST Cybersecurity Framework", "kind": "cybersecurity-framework", "coverage_label": "Expliciete partiële crosswalk"},
    {"id": "cvss", "name": "CVSS", "kind": "vulnerability-scoring-context", "coverage_label": "Context-only"},
)


def _external_frameworks(crosswalk: dict[str, object]) -> list[dict[str, object]]:
    controls = cast(list[dict[str, object]], crosswalk["controls"])
    mappings = [mapping for control in controls for mapping in cast(list[dict[str, object]], control["mappings"])]
    result: list[dict[str, object]] = []
    for meta in _FRAMEWORK_META:
        framework_mappings = [item for item in mappings if item["framework_id"] == meta["id"]]
        if meta["id"] == "cvss":
            coverage = "context_only"
            note = "CVSS is expliciet als scoring-context gemapt en blijft gescheiden van compliance- en lokale exposureclaims."
        elif framework_mappings:
            coverage = "mapped_partial"
            note = f"{len(framework_mappings)} expliciete typed repository-backed relaties; dit is een partiële crosswalk en geen certificering of blanket compliance."
        else:
            coverage = "unmapped"
            note = "Geen expliciete repository-backed relatie beschikbaar; DTMO leidt geen equivalentie af."
        result.append({
            **meta,
            "coverage": coverage,
            "mapping_ids": [str(item["object_id"]) for item in framework_mappings],
            "note": note,
            "provenance": ["backend/dtmo/governance_crosswalk.py", "docs/governance/GOVERNANCE_MAPPING_REGISTRY.md"],
        })
    return result


def governance_snapshot() -> dict[str, object]:
    crosswalk = control_crosswalk()
    frameworks = _external_frameworks(crosswalk)
    frameworks.append({
        "id": "dtmo-governance",
        "name": "DTMO security & release governance",
        "kind": "internal-governance",
        "coverage": "mapped_internal",
        "coverage_label": "Repository-backed",
        "mapping_ids": [str(item["id"]) for item in _INTERNAL_MAPPINGS],
        "note": "Interne governancegrenzen zijn rechtstreeks traceerbaar naar repository-evidence.",
        "provenance": ["docs/security/SECURITY_OVERVIEW.md", "docs/traceability/TRACEABILITY_MATRIX.md"],
    })
    return {
        "status": "repository_backed",
        "frameworks": frameworks,
        "mappings": [dict(item) for item in _INTERNAL_MAPPINGS],
        "control_crosswalk": crosswalk,
        "authority_boundaries": list(_AUTHORITY_BOUNDARIES),
        "claim_boundary": "External framework relationships are displayed only when explicitly defined in the repository crosswalk. Typed partial mappings do not constitute certification, full compliance, semantic equivalence, environment effectiveness or production authorization.",
    }


@router.get("/knowledge")
def governance_knowledge(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
) -> dict[str, object]:
    del principal
    return governance_snapshot()
