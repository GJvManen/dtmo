# DTMO Roadmap — Production Readiness and Product Evolution

Last updated: **2026-08-15**

## Purpose

This roadmap separates production authorization from product evolution. Repository engineering, external staging acceptance, independent assurance and the final production decision are distinct evidence classes and must not be conflated.

## Current position

| Stage | Scope | Status |
|---|---|---|
| Phases 1–7 | Repository-controlled engineering baseline | `PASS` |
| RC13 + owner retest | Unified-console functional acceptance | `PASS / OWNER_ACCEPTED` |
| E8.1–E8.10 | Vulnerability & CTI ecosystem integrations | `PASS / REPOSITORY_COMPLETE` |
| Phase 8.2–8.4 | Platform/identity, source-to-intelligence, operations/recovery | `PASS` |
| Phase 8.5 | Accountable production-equivalent staging acceptance | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Independent external assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Formal production go/no-go | `IN PROGRESS / DECISION REQUIRED` |

DTMO has completed the staging and independent-assurance prerequisites. It is **not production authorized until Phase 10 records an accountable GO decision**.

# Track A — Production readiness

## Phase 8 — production-equivalent staging acceptance

**Status:** `PASS / OWNER_ACCEPTED`

Phase 8.2 through Phase 8.5 are reported complete and accepted by the accountable owner. The accepted evidence remains external/restricted evidence where applicable; repository CI is supporting engineering evidence and is not retrospectively promoted to external staging evidence.

## Phase 9 — independent external assurance

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED`

Independent external assurance is reported complete, including disposition/retest of release-blocking findings as required for acceptance. Historical Phase 9 preparation contracts remain useful evidence structure, but the accepted external assurance decision is the authoritative prerequisite for Phase 10.

## Phase 10 — formal production go/no-go

**Status:** `IN PROGRESS / ACCOUNTABLE PRODUCTION DECISION REQUIRED`

Phase 10 is the active gate. Required decision inputs are:

1. accepted Phase 8 staging evidence and accountable acceptance;
2. accepted Phase 9 independent assurance;
3. approved production environment, accountable service owner and support model;
4. immutable production release identity and image digests;
5. approved IAM, service identities, secrets management and network controls;
6. approved backup, restore, recovery and rollback arrangements;
7. approved monitoring, alerting, on-call and escalation model;
8. incident-response/security-operations handover;
9. privacy, data-handling, legal and governance approval;
10. open-finding statement and accountable residual-risk disposition;
11. formal production release/change authorization;
12. recorded go-live window and rollback authority.

### Decision rule

Phase 10 is fail-closed. Any missing required approval, unresolved release-blocking finding, unaccepted residual risk, or material mismatch between the approved and intended production release identity results in `NO-GO / BLOCKED` until corrected and, where necessary, revalidated.

A `GO` applies only to the recorded immutable production release identity. A material candidate change after accepted Phase 8/9 evidence requires an explicit impact assessment and appropriate revalidation before production authorization.

See `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md` for the formal decision record requirements.

### Post-GO

A production `GO` is followed by controlled deployment, release-identity verification, health/readiness verification, monitoring/alert confirmation, change closure and confirmation that rollback and incident escalation remain available. Production authorization does not grant autonomous publication or external-sharing authority.

# Track B — Product evolution

The accepted repository baseline includes the unified console, governed source operations, severity/classification semantics, vulnerability analytics, explicit governance mappings, Administration/RBAC, OpenCVE and CIRCL Vulnerability-Lookup, governed MISP read/export, governed AIL read/enrichment/correlation and the published governed UI-01–UI-10 documentation baseline.

Further product evolution must not silently change the candidate under Phase 10. Material release changes require explicit impact assessment and may trigger staging or assurance revalidation.

# Delivery and documentation discipline

Professional documentation records stable product, architecture, security, governance and current readiness state. Historical run records remain immutable and scoped to the state they covered. External/restricted evidence is referenced rather than copied when it contains sensitive operational information.

Every material release change requires bounded scope, acceptance criteria, applicable exact-head CI and an explicit decision on whether existing staging/assurance evidence remains applicable.

## Immediate next steps

1. Complete the Phase 10 production decision package.
2. Record production environment/owner/support approval and immutable production release identity.
3. Confirm IAM/secrets/network, recovery/rollback, monitoring/on-call/escalation, incident-response and privacy/legal approvals.
4. Confirm no unresolved release blocker remains and record residual-risk disposition.
5. Record the accountable Phase 10 `GO` or `NO-GO / BLOCKED` decision.
6. On `GO`, execute controlled production deployment and post-deployment verification.