# Phase 8 Staging Deployment-Parity Gate

## Decision

`BLOCKED_EXTERNAL`

## Objective

Require independently observable, production-equivalent staging deployment evidence before any staging acceptance suite is treated as valid.

## Latest reconciliation

The repository-controlled staging-emulator configuration contract is accepted from PR #104 evidence. The bounded application-container runtime smoke is now also accepted from PR #107 exact-head evidence: final head `52d7a37660c9bb1c9f8468f11010f36d17bd1fba` completed 48/48 workflows successfully and merged as `23d629964f55709845683e808f707998cc8d4aa2`; retained artifact `9057259246` is exact-head bound with machine-readable PASS, contract JUnit 4/4 and runtime JUnit 12/12.

RUN-156 performed a fresh repository and issue review for one approved real staging deployment and a complete ten-class deployment-parity package. No reviewable evidence tied to one immutable real staging deployment identity was found. Repository CI, emulator configuration evidence and bounded application-container runtime smoke therefore remain non-substitutive for this gate.

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

All ten evidence classes must be retained, reviewable and tied to the same staging deployment identity. Missing, stale, inaccessible, contradictory or inferred evidence blocks staging acceptance. Repository CI, emulator configuration evidence or bounded application-container runtime smoke cannot substitute for a real deployed environment.

No real staging smoke, integration, migration, connector, recovery, performance, accessibility or observability result is valid for Phase 8 until this gate is satisfied.

## Governance and privacy

- RBAC and separation of duties remain unchanged.
- Human share approval remains a separate human authority.
- Staging access does not grant publication authority.
- Secret values, tokens, credentials and unnecessary personal data are excluded from repository evidence.
- Provenance and immutable deployment identity are mandatory.

## Threat/advisory provenance rule

Evidence class 10 must be produced against the actual immutable staged release and must preserve source provenance, review time and confidence for relevant public threat intelligence, CVE data and vendor advisories. A generic or pre-deployment advisory review does not close this class.

## Exactly one next priority

Provide or provision one approved real staging deployment and retain all ten deployment-parity evidence classes against one immutable staging deployment identity. Do not begin or credit the staging acceptance suite before this gate is complete.
