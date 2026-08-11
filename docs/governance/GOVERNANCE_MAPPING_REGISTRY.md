# DTMO Governance Mapping Registry

Last updated: 2026-08-11

## Purpose

This registry is the repository authority for the governance knowledge surface exposed by RC13.4. It records what DTMO can actually trace to repository evidence and, equally importantly, which external framework crosswalks do **not** yet exist.

## Claim rule

DTMO must never infer a framework/control/technique equivalence merely because two concepts appear related. A framework is shown as mapped only when the repository contains an explicit mapping identifier plus provenance for that mapping. Missing mappings stay visibly missing.

## External framework coverage

| Framework | DTMO use | Current coverage | Mapping identifiers | Repository evidence |
|---|---|---|---|---|
| Normenkader IBP | Education-sector information-security governance context | `UNMAPPED` | None | RC13 functional-acceptance requirement only; no control-level crosswalk dataset exists yet |
| MITRE ATT&CK | Threat-behavior/tactic/technique context | `UNMAPPED` | None | RC13 functional-acceptance requirement only; no technique-level mapping dataset exists yet |
| CVSS | Vulnerability-scoring context | `CONTEXT_ONLY` | None | `backend/dtmo/api/schemas.py` exposes canonical `severity` and free `metadata`, but no first-class CVSS vector/base-score field |

The absence of a mapping is intentional evidence, not an invitation to infer one in the UI.

## Repository-backed DTMO governance mappings

These are internal DTMO governance controls, not claims of equivalence to Normenkader IBP, MITRE ATT&CK or CVSS.

| Mapping ID | Control area | Authoritative source | Section / evidence |
|---|---|---|---|
| `identity-access` | RBAC and least privilege | `docs/security/SECURITY_OVERVIEW.md` | Identity and access control |
| `separation-of-duties` | Review/share and technical authority separation | `docs/security/SECURITY_OVERVIEW.md` | Separation of duties |
| `privacy-provenance` | Data minimisation, source provenance, confidence and secret handling | `docs/security/SECURITY_OVERVIEW.md` | Data protection and privacy |
| `exact-head-evidence` | Exact-head evidence requirement for acceptance claims | `docs/traceability/TRACEABILITY_MATRIX.md` | Traceability rule |
| `external-assurance-boundary` | Repository evidence does not prove real staging/external assurance/production acceptance | `docs/traceability/TRACEABILITY_MATRIX.md` | Phase 8/9/10 rows |
| `threat-vulnerability-management` | Target-bound CVE/vendor advisory review with provenance/applicability/confidence | `docs/security/SECURITY_OVERVIEW.md` | Threat and vulnerability management |

## Authority boundaries surfaced in the console

1. Dashboard or console visibility never grants publication/share authority.
2. Human review and external share approval remain separate authorities.
3. Service accounts/connectors do not receive human approval powers.
4. Missing, stale, inferred or inaccessible evidence is not a PASS.
5. RC13 must complete before Phase 8 external staging readiness is restored.

## Runtime contract

`GET /api/v1/governance/knowledge` exposes the registry as a read-only authenticated knowledge snapshot. The canonical Governance tab renders framework coverage, repository-backed mappings and authority boundaries. RC13.4 does not add write paths, dynamic mapping creation or external publication authority.

## Future mapping work

A future change may add curated Normenkader IBP control IDs, MITRE ATT&CK technique IDs or first-class CVSS fields only when each mapping is represented in an explicit versioned dataset with source/version provenance and dedicated review. That future work must be additive and must not rewrite historical evidence.
