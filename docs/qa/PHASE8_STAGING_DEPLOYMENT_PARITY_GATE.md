# Phase 8 Staging Deployment-Parity Gate

## Decision

`PAUSED_PENDING_RC13_REPAIR_AND_OWNER_RETEST`

## Objective

Require independently observable, production-equivalent staging deployment evidence before staging acceptance can be declared, but only after the canonical local product has a current accountable functional acceptance.

## Entry condition — reopened

RC13.1–RC13.5 repository evidence and the earlier project-owner acceptance remain historical evidence. However, a **subsequent project-owner functional retest on 2026-08-12 reported new blocking canonical-console defects**.

Issue #150 is therefore reopened and authoritative.

The current RC13 entry condition is **not satisfied** until all of the following are true:

1. the reopened Overview refresh/usability defects are repaired;
2. zero-data status and graph semantics are truthful;
3. Chrome button/navigation interaction evidence succeeds without browser page/console errors;
4. Administration is presented as a clear governed workspace;
5. the complete repair passes exact-head CI and merges;
6. the accountable project owner explicitly retests and accepts the repaired local product again.

## Phase 8.1 external deployment identity

PR #157 remains valid historical repository evidence and the fail-closed intake record remains at `docs/staging/PHASE8_DEPLOYMENT_IDENTITY_RECORD.md`.

No real production-equivalent staging deployment identity has been accepted. Issue #158 is paused while RC13 is reopened.

Do not provision, credit or accept Phase 8 evidence against the current product while this gate is paused.

## Required external evidence when Phase 8 resumes

All evidence must be tied to the **same immutable staging deployment identity**:

1. approved staging environment identifier and accountable owner;
2. reachable staging endpoint through the approved access path;
3. immutable deployed application/container image digests and release identity;
4. infrastructure/runtime versions and configuration-parity evidence;
5. approved secrets-manager/identity references and least-privilege staging identities, with no secret values committed;
6. TLS certificate/termination and network-restriction evidence;
7. production-equivalent data-class/sanitization statement and explicit no-production-credential confirmation;
8. deployment log/change record tied to the immutable release identity;
9. rollback target/procedure tied to the staged release;
10. deployment-time security/CVE/vendor-advisory review evidence.

## Acceptance rule

Phase 8 becomes `PASS` only when the current RC13 functional owner gate is accepted and all external staging evidence is reviewable and consistently tied to one immutable production-equivalent deployment identity, deployed-environment acceptance suites succeed, and the project owner records external staging acceptance.

Missing, stale, inaccessible, contradictory or inferred evidence blocks acceptance.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access or Governance visibility does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity remain mandatory.

## Exactly one next priority

**Paused. Complete issue #150 canonical-console repair and accountable project-owner retest before Phase 8.1 may resume.**
