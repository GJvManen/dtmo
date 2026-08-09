# Phase 8 Staging Deployment-Parity Gate

## Decision

`BLOCKED_EXTERNAL`

## Objective

Require independently observable, production-equivalent staging deployment evidence before any staging acceptance suite is treated as valid.

## Latest reconciliation

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 registered workflows successfully; retained emulator artifact `9045039742` was exact-head bound with machine-readable PASS and JUnit 4/4; PR #104 merged as `3c7a4b7f56e8d8a757541963bbd261fe42a7269c`. The repository-controlled emulator configuration/topology baseline is therefore accepted.

RUN-153 adds a bounded runtime smoke for the actual DTMO application container. Even if RUN-153 passes, application-container runtime evidence does not satisfy this gate because it does not prove the complete dependency topology or a real deployed staging environment.

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

All ten evidence classes must be retained, reviewable and tied to the same staging deployment identity. Missing, stale, inaccessible, contradictory or inferred evidence blocks staging acceptance. Repository CI, emulator configuration evidence or bounded runtime-smoke evidence cannot substitute for a real deployed environment.

No smoke, integration, migration, connector, recovery, performance, accessibility or observability result is credited as real staging acceptance until this gate is satisfied.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Exactly one next priority

Verify RUN-153 exact-head CI and retained runtime evidence. After acceptance, complete dependency-topology emulation or provide/provision the approved real staging environment; all ten evidence classes remain mandatory for real Phase 8 staging acceptance.
