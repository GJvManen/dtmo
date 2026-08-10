# Phase 8 Staging Deployment-Parity Gate

## Decision

`BLOCKED_EXTERNAL`

## Objective

Require independently observable, production-equivalent staging deployment evidence before any staging acceptance suite is treated as valid.

## Latest reconciliation

RUN-150 / PR #103 exact head `be9deb34255f6114430d76868c9bf82f0e039f15` completed 46/46 registered workflows successfully and merged as `1e957f7fa1e9910e5d258cd6d7ed5ce69e9203d1`. A fresh repository and issue #1 review found no real staging environment or deployment-parity evidence.

RUN-151 added the source-controlled production-equivalent staging emulator contract. RUN-152 repaired its governance-document wording defect, and PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 workflows successfully. Retained emulator artifact `9045039742` is exact-head bound and internally consistent, so the emulator gate is accepted as `PASS` for configuration-contract scope only.

That acceptance does not satisfy this deployment-parity gate. The retained emulator evidence itself explicitly records that containers were not executed, a real staging environment was not proven, deployment parity was not proven, the ten external evidence classes were not satisfied, Phase 8 was not completed and production acceptance was not completed.

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

Verify the RUN-153 documentation reconciliation PR on its exact final head and merge only on complete CI success. After that merge, provide or provision the approved real staging environment and retain all ten deployment-parity evidence classes against one immutable staging deployment identity.
