# Phase 8 Staging Deployment-Parity Gate

## Decision

`BLOCKED_EXTERNAL`

## Objective

Require independently observable, production-equivalent staging deployment evidence before any staging acceptance suite is treated as valid.

## Latest reconciliation

RUN-150 / PR #103 exact head `be9deb34255f6114430d76868c9bf82f0e039f15` completed 46/46 registered workflows successfully and merged as `1e957f7fa1e9910e5d258cd6d7ed5ce69e9203d1`. A fresh repository and issue #1 review still found no real staging environment or deployment-parity evidence.

RUN-151 adds a source-controlled production-equivalent staging emulator contract. RUN-152 repaired a governance-document wording defect after RC4 failed on the first emulator head. Even if the emulator CI gate ultimately passes, emulator configuration evidence does not satisfy this gate because it does not prove a real deployed environment or runtime behavior.

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

All ten evidence classes must be retained, reviewable and tied to the same staging deployment identity. Missing, stale, inaccessible, contradictory or inferred evidence blocks staging acceptance. Repository CI or emulator configuration evidence cannot substitute for a real deployed environment.

No smoke, integration, migration, connector, recovery, performance, accessibility or observability staging result is valid for Phase 8 until this gate is satisfied.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Exactly one next priority

Verify RUN-151/RUN-152 on the changed PR #104 exact head. Merge only after complete CI and retained emulator evidence; then provide or provision the approved real staging environment and retain all ten deployment-parity evidence classes.
