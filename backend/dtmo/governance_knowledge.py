from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from dtmo.auth.dependencies import require_permission
from dtmo.auth.policy import Permission, Principal

router = APIRouter(prefix="/api/v1/governance", tags=["governance"])

_FRAMEWORKS: tuple[dict[str, object], ...] = (
    {
        "id": "normenkader-ibp",
        "name": "Normenkader IBP",
        "kind": "education-security-framework",
        "coverage": "unmapped",
        "coverage_label": "Nog niet gemapt",
        "mapping_ids": [],
        "note": (
            "DTMO heeft nog geen repository-backed control-level Normenkader IBP crosswalk. "
            "RC13.4 toont dit expliciet en leidt geen control-equivalenties af."
        ),
        "provenance": ["docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"],
    },
    {
        "id": "mitre-attack",
        "name": "MITRE ATT&CK",
        "kind": "threat-behavior-taxonomy",
        "coverage": "unmapped",
        "coverage_label": "Nog niet gemapt",
        "mapping_ids": [],
        "note": (
            "Er is geen repository-backed technique-level ATT&CK mappingdataset. "
            "DTMO claimt daarom geen techniekmapping op basis van vrije tags of metadata."
        ),
        "provenance": ["docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md"],
    },
    {
        "id": "cvss",
        "name": "CVSS",
        "kind": "vulnerability-scoring-context",
        "coverage": "context_only",
        "coverage_label": "Context, geen first-class score",
        "mapping_ids": [],
        "note": (
            "De canonical ingest heeft een severity-veld en vrije metadata, maar geen first-class "
            "CVSS vector/base-score veld. RC13.4 presenteert CVSS daarom uitsluitend als context."
        ),
        "provenance": ["backend/dtmo/api/schemas.py"],
    },
    {
        "id": "dtmo-governance",
        "name": "DTMO security & release governance",
        "kind": "internal-governance",
        "coverage": "mapped_internal",
        "coverage_label": "Repository-backed",
        "mapping_ids": [
            "identity-access",
            "separation-of-duties",
            "privacy-provenance",
            "exact-head-evidence",
            "external-assurance-boundary",
            "threat-vulnerability-management",
        ],
        "note": "Interne governancegrenzen zijn rechtstreeks traceerbaar naar repository-evidence.",
        "provenance": [
            "docs/security/SECURITY_OVERVIEW.md",
            "docs/traceability/TRACEABILITY_MATRIX.md",
        ],
    },
)

_MAPPINGS: tuple[dict[str, object], ...] = (
    {
        "id": "identity-access",
        "title": "Identity & access control",
        "statement": "RBAC en least privilege zijn verplicht; service accounts krijgen geen human review/share authority.",
        "source": "docs/security/SECURITY_OVERVIEW.md",
        "section": "Identity and access control",
    },
    {
        "id": "separation-of-duties",
        "title": "Separation of duties",
        "statement": "Technische toegang, deployment, CI of operations impliceert geen publication/share approval.",
        "source": "docs/security/SECURITY_OVERVIEW.md",
        "section": "Separation of duties",
    },
    {
        "id": "privacy-provenance",
        "title": "Privacy, provenance & confidence",
        "statement": "Dataminimalisatie, bronprovenance en confidence moeten behouden blijven; secrets horen niet in repository of evidence.",
        "source": "docs/security/SECURITY_OVERVIEW.md",
        "section": "Data protection and privacy",
    },
    {
        "id": "exact-head-evidence",
        "title": "Exact-head release evidence",
        "statement": "Een PASS-claim vereist uitvoerbare exact-head evidence; workflowdefinitie alleen is onvoldoende.",
        "source": "docs/traceability/TRACEABILITY_MATRIX.md",
        "section": "Traceability rule",
    },
    {
        "id": "external-assurance-boundary",
        "title": "External assurance boundary",
        "statement": "Repository emulator/runtime evidence bewijst geen real staging, pentest of production acceptance.",
        "source": "docs/traceability/TRACEABILITY_MATRIX.md",
        "section": "Phase 8/9/10 rows",
    },
    {
        "id": "threat-vulnerability-management",
        "title": "Threat & vulnerability management",
        "statement": "CVE/vendor advisory beoordeling moet doelgebonden zijn en provenance, tijd, applicability en confidence vastleggen.",
        "source": "docs/security/SECURITY_OVERVIEW.md",
        "section": "Threat and vulnerability management",
    },
)

_AUTHORITY_BOUNDARIES: tuple[str, ...] = (
    "Dashboard- of consolezichtbaarheid verleent geen publication/share authority.",
    "Human review en externe share approval blijven afzonderlijke bevoegdheden.",
    "Service accounts/connectors krijgen geen human approval powers.",
    "Ontbrekende, stale, inferred of inaccessible evidence telt niet als PASS.",
    "RC13 completion is vereist voordat Phase 8 external staging readiness kan worden hersteld.",
)


def governance_snapshot() -> dict[str, object]:
    return {
        "status": "repository_backed",
        "frameworks": [dict(item) for item in _FRAMEWORKS],
        "mappings": [dict(item) for item in _MAPPINGS],
        "authority_boundaries": list(_AUTHORITY_BOUNDARIES),
        "claim_boundary": (
            "External framework crosswalks are never inferred. Only mappings with explicit repository provenance are displayed as mapped."
        ),
    }


@router.get("/knowledge")
def governance_knowledge(
    principal: Annotated[Principal, Depends(require_permission(Permission.READ_INTELLIGENCE))],
) -> dict[str, object]:
    del principal
    return governance_snapshot()
