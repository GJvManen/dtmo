# DTMO Document Control Register

## Purpose

This register identifies the principal professional documents used to describe and govern DTMO. It is a navigation and ownership aid, not a substitute for Git history or acceptance evidence.

## Document classes

| Class | Purpose | Typical update trigger |
|---|---|---|
| Executive | Decision-oriented status and readiness | Material readiness or risk change |
| Product | Accepted capability and limitations | Material product behavior change |
| Architecture | Components, flows and trust boundaries | Architectural or dependency change |
| Security | Identity, authorization and security controls | Security-model or control change |
| Governance | Authority, mapping and evidence rules | Governance/control model change |
| Operations | Deployment and service operation | Operational procedure or topology change |
| QA / assurance | Acceptance criteria and gate evidence | Gate, test or acceptance change |
| Release | Version-specific release information | Release publication |
| Development evidence | Point-in-time implementation history | Engineering/acceptance run |

## Principal controlled documents

| Document | Class | Primary purpose | Authority |
|---|---|---|---|
| `README.md` | Product | Public project entry point and current high-level baseline | Repository baseline |
| `docs/README.md` | Product | Professional documentation portal | Documentation baseline |
| `docs/project/EXECUTIVE_STATUS.md` | Executive | Leadership status and decision context | Project/readiness status |
| `docs/project/CURRENT_STATE.md` | Product | Current accepted capabilities and limitations | Product baseline |
| `docs/project/PROJECT_GOVERNANCE.md` | Governance | Ownership, authority, evidence and release governance | Governance baseline |
| `docs/project/DOCUMENTATION_STANDARD.md` | Governance | Documentation quality and maintenance rules | Documentation governance |
| `docs/project/GLOSSARY.md` | Governance | Canonical terminology | Terminology baseline |
| `docs/architecture/SYSTEM_ARCHITECTURE.md` | Architecture | Logical architecture, data flow and trust boundaries | Architecture baseline |
| `docs/security/SECURITY_OVERVIEW.md` | Security | Security model and authority boundaries | Security baseline |
| `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md` | Governance | Explicit framework mapping truth | Mapping authority |
| `docs/traceability/TRACEABILITY_MATRIX.md` | Governance | Requirement/control/evidence traceability | Traceability authority |
| `docs/qa/QA_AND_RELEASE_GATES.md` | QA / assurance | Consolidated acceptance-gate model | QA/release baseline |
| `docs/project/PRODUCTION_READINESS_REPORT.md` | Executive / QA | Consolidated production-readiness position | Readiness baseline |
| `docs/project/PRODUCTION_CHECKLIST.md` | QA / assurance | Evidence checklist for progression | Readiness evidence control |
| `docs/roadmap/PRODUCTION_ROADMAP.md` | Product / QA | Planned route to production decision | Roadmap baseline |
| `docs/operations/OPERATIONS_MANUAL.md` | Operations | Operational procedures | Operations baseline |
| `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md` | QA / assurance | Immutable Phase 8 deployment identity intake | Phase 8 environment evidence |
| `docs/evidence/EVIDENCE_INDEX.md` | QA / assurance | Structured evidence navigation | Evidence index |

## Status vocabulary

Professional documents should use unambiguous state language. Preferred states include:

- `PLANNED` — approved or proposed work not yet implemented;
- `IMPLEMENTED` — capability exists but required acceptance may be incomplete;
- `PASS` — defined acceptance criteria are satisfied by attributable evidence;
- `OWNER_ACCEPTED` — accountable owner acceptance has been explicitly recorded where required;
- `READY_FOR_EXTERNAL_VALIDATION` — repository prerequisites are met, but external/environment acceptance is not complete;
- `NOT COMPLETE` — required evidence remains outstanding;
- `NOT STARTED` — the governed activity has not begun;
- `BLOCKED` — progression cannot continue until an identified blocker is resolved.

Avoid ambiguous labels such as "done", "looks good", "production-like" or "ready" without a defined gate and evidence boundary.

## Version and evidence control

Git history provides document version history. Acceptance claims must additionally identify the commit, release or deployment to which they apply when that identity is material. Point-in-time CI and runtime evidence should be linked or indexed rather than copied into multiple stable documents.

## Review expectations

A documentation change requires technical review when it changes architecture or implementation claims; security/governance review when it changes authority, control or assurance claims; and product/readiness review when it changes accepted capability or progression status.

Documentation-only changes must still pass applicable repository quality gates. Documentation changes do not by themselves establish environment or independent assurance.
