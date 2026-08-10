# Phase 8 Staging Deployment-Parity Gate

## Decision

`BLOCKED_EXTERNAL`

## Objective

Require independently observable, production-equivalent staging deployment evidence before any staging acceptance suite is treated as valid.

## Latest reconciliation

The repository-controlled staging-emulator configuration contract is accepted from PR #104 evidence. PR #106 final exact head `ff0a490e46c2f9529441d8a5294030af498dbe14` completed 47/47 workflows and merged as `b57a6daa775d2f1f88a2d1b67b191da757fa743f`, finalizing its documentation reconciliation.

RUN-155 now carries forward the bounded DTMO application-container runtime smoke from stale PR #105 onto current `main`. Even if that runtime-smoke gate passes, it executes only the DTMO application container and therefore does not satisfy this deployment-parity gate.

## Required external evidence

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

All ten evidence classes must be retained, reviewable and tied to the same staging deployment identity. Missing, stale, inaccessible, contradictory or inferred evidence blocks staging acceptance. Repository CI, emulator configuration evidence, or bounded application-container runtime smoke cannot substitute for a real deployed environment.

No real staging smoke, integration, migration, connector, recovery, performance, accessibility or observability result is valid for Phase 8 until this gate is satisfied.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Exactly one next priority

Verify the RUN-155 runtime-smoke PR on its exact final head and independently inspect retained runtime evidence. After that bounded gate is accepted, provide or provision the approved real staging environment and retain all ten deployment-parity evidence classes against one immutable staging deployment identity.
