# DTMO Governance Mapping Registry

Last updated: **2026-08-12**

## Purpose

This registry is the current repository authority for governance/framework mapping claims exposed by DTMO. It records both what DTMO can explicitly trace to evidence and what is not yet mapped.

The registry remains authoritative until the planned first-class framework mapping data/API model replaces the repository-only representation.

## Claim rule

DTMO must never infer a framework/control/technique equivalence merely because concepts appear related.

A mapping is considered valid only when it has an explicit identifier/relationship plus provenance sufficient for review. Missing mappings remain visibly missing.

## External framework coverage

| Framework | DTMO use | Current coverage | First-class mapping identifiers | Current evidence |
|---|---|---|---|---|
| Normenkader IBP | Education-sector information-security governance context | `UNMAPPED` | None | No complete control-level crosswalk dataset exists yet |
| MITRE ATT&CK | Threat behavior, tactic and technique context | `UNMAPPED` | None | No complete technique-level mapping dataset exists yet |
| CVSS | Vulnerability severity/scoring context | `CONTEXT_ONLY` | None | Canonical severity/context exists, but no complete first-class CVSS vector/base-score mapping model yet |

The absence of a mapping is intentional evidence, not an invitation to infer one in the UI or analytics.

## Repository-backed DTMO governance mappings

These are internal DTMO governance/control relationships, not claims of equivalence to Normenkader IBP, MITRE ATT&CK or CVSS.

| Mapping ID | Control area | Authoritative source | Evidence focus |
|---|---|---|---|
| `identity-access` | RBAC and least privilege | `docs/security/SECURITY_OVERVIEW.md` | Identity, authentication and authorization |
| `separation-of-duties` | Review/share and technical authority separation | `docs/security/SECURITY_OVERVIEW.md` | Separation of duties / publication authority |
| `privacy-provenance` | Data minimization, provenance, confidence and secret handling | `docs/security/SECURITY_OVERVIEW.md` | Data protection and source/evidence integrity |
| `exact-head-evidence` | Exact-head acceptance discipline | `docs/qa/QA_AND_RELEASE_GATES.md` | Release evidence rules |
| `external-assurance-boundary` | Repository evidence is distinct from real staging/assurance/production approval | `docs/project/PRODUCTION_READINESS_REPORT.md` | Phase 8/9/10 evidence boundary |
| `threat-vulnerability-management` | Target-bound CVE/vendor-advisory review | `docs/security/SECURITY_OVERVIEW.md` | Threat and vulnerability management |
| `functional-owner-acceptance` | Repository functional evidence plus accountable owner acceptance | `docs/qa/RC13_FUNCTIONAL_CONSOLE_ACCEPTANCE_GATE.md` | Functional product acceptance |
| `staging-deployment-identity` | Immutable staging identity and least-privilege evidence | `docs/qa/PHASE8_STAGING_DEPLOYMENT_PARITY_GATE.md` | Phase 8 staging boundary |

## Authority boundaries surfaced by Governance

1. Dashboard/console visibility never grants publication/share authority.
2. Human review and external-share approval remain separate authorities.
3. Service accounts/connectors do not receive human approval powers.
4. Missing, stale, inferred or inaccessible evidence is not `PASS`.
5. Governance knowledge is descriptive/evidentiary and does not create authorization.
6. Framework coverage must remain truthful when mappings are absent.

## Runtime contract

`GET /api/v1/governance/knowledge` exposes a read-only authenticated governance knowledge snapshot. The canonical Governance area renders framework coverage, repository-backed internal mappings and authority boundaries.

The current baseline does not provide arbitrary framework-mapping write paths through the Governance UI.

## Planned first-class framework mapping model

The post-RC13 enhancement roadmap will move mapping truth from repository-only knowledge into an explicit canonical model.

A future mapping record should include at minimum:

- mapping ID;
- framework name;
- framework version;
- control/technique/rule identifier;
- mapping target/type/relationship;
- source/provenance reference;
- confidence/status;
- review state;
- reviewer/authorization context;
- creation/update timestamps;
- version/history where relevant.

### Initial mapping targets

The first implementation should consider:

- Normenkader IBP controls relevant to DTMO security/governance capabilities;
- MITRE ATT&CK tactic/technique relationships for intelligence records where explicit evidence exists;
- structured CVSS fields/context where supplied by sources and appropriate for the canonical model.

### Governance UI evolution

Once the canonical mapping model exists, Governance should be able to provide:

- framework/version inventory;
- mapped/unmapped coverage counts;
- evidence/provenance visibility;
- review state;
- drill-down from framework control/technique to mapped DTMO control/intelligence/evidence;
- clear distinction between normative requirement, internal control implementation, threat-intelligence relationship and evidence.

The Governance UI must continue to display `UNMAPPED`/`CONTEXT_ONLY` where appropriate and must never fill gaps through semantic inference.

## Current lifecycle context

RC13 functional acceptance is complete. Phase 8 real staging is now the active production-readiness gate.

The framework-mapping expansion is a product enhancement and does not itself constitute Phase 8/9/10 acceptance evidence unless explicitly validated within those environments/gates.
