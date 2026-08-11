# Phase 8 Staging Deployment-Parity Gate

## Decision

`PAUSED_PENDING_RC13`

## Objective

Require independently observable, production-equivalent staging deployment evidence before staging acceptance can be declared.

The repository-controlled engineering baseline remains accepted through Phase 7, but project-owner functional testing on 2026-08-11 inserted RC13 as a blocking product-acceptance programme. The earlier `READY_FOR_EXTERNAL_VALIDATION` handoff remains withdrawn until RC13 reaches `PASS`.

## Entry condition

Do not begin or credit Phase 8 external validation until all of the following are true:

1. RC13.1 source-to-intelligence path is accepted;
2. RC13.2 single-session Visual analytics is accepted;
3. RC13.3 governed Administration/RBAC is accepted;
4. RC13.4 Governance knowledge surface is accepted;
5. RC13.5 complete canonical-console browser acceptance succeeds on one exact head;
6. the project owner confirms the repaired product is functionally suitable to move to external staging validation.

RC13.1 is accepted via PR #151. RC13.2 is accepted via PR #152 (`b8c254c5d099cde5dca624aa85b17c320594847e`). RC13.3 is accepted via PR #153 (`2e1029a43f7b44d8525fb89197d0a10458a3e992`). **RC13.4 Governance knowledge is now the current priority**, so the Phase 8 entry condition remains unmet.

## Required external evidence

When the entry condition is met, all evidence must be tied to the **same immutable staging deployment identity**:

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

Phase 8 becomes `PASS` only when the RC13 entry condition is complete and all ten evidence classes are reviewable and consistently tied to one immutable staging deployment identity.

Missing, stale, inaccessible, contradictory or inferred evidence blocks acceptance. Repository CI, Docker Compose, staging-emulator configuration and application-container smoke tests are supporting engineering evidence only and cannot substitute for a real deployed environment.

## Identity/RBAC staging requirement

When Phase 8 reopens, the staging deployment must demonstrate that externally issued bearer-token roles reconcile with the governed managed principal/role assignments and the accepted identity-provider process. Staging must not rely on development header-based identity or assume that a database assignment silently rewrites an active bearer token.

## Governance staging requirement

The canonical Governance surface must remain read-only and preserve the accepted mapping truth boundary. External framework/control/technique mappings may not be promoted from `UNMAPPED`/`CONTEXT_ONLY` without explicit versioned repository evidence and provenance.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access or Governance visibility does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Exactly one next priority

Phase 8 has **no executable next action while paused**. The project priority is **RC13.4 — repository-backed Governance knowledge** under issue #150 and the RC13 functional console acceptance gate.
