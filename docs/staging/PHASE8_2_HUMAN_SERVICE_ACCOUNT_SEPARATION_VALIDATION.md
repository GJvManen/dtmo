# Phase 8.2.8 — Human / Service-account Separation Validation

## Purpose

Validate that DTMO keeps human interactive identities and non-human service accounts operationally and cryptographically separated on the owner-approved post-E8 production-equivalent staging deployment.

Repository CI and synthetic fixtures are supporting evidence only. `PASS` requires evidence from the approved staging deployment and must be attributable to the same immutable Phase 8.2 deployment identity.

## Preconditions

- Phase 8.2 is active on `main`.
- The deployment identity has an environment identifier, exact deployed Git commit, immutable application image digest and deployment fingerprint.
- The same deployment fingerprint is used for every accepted Phase 8.2 step.
- Test identities are staging-only; production human or service-account credentials are not reused.

## Validation procedure

1. Identify at least one representative human interactive identity and one representative non-human service account used by DTMO.
2. Demonstrate that the identities are distinct principals with separately managed credentials or trust material.
3. Verify that the service account cannot perform interactive human login unless such behavior is explicitly designed, documented and approved.
4. Verify that human accounts are not reused for connector, scheduler, worker, ingestion or other background service execution.
5. Inspect effective service-account permissions and confirm least-privilege scope for the intended workload.
6. Confirm service credentials are separately managed and rotatable without requiring distribution to human users.
7. Perform a safe staging-only disable/revoke test and confirm the affected service identity loses access as designed without changing the human identity.
8. Confirm audit records distinguish the human principal from the service principal for representative actions.
9. Confirm authentication/authorization failures are observable without recording secrets or raw credential material.
10. Record reviewer, timestamp and restricted evidence reference, then bind the result to the Phase 8.2 deployment fingerprint.

## Required evidence

- environment/deployment fingerprint;
- exact deployed commit and application image digest;
- identifiers for representative human and service principals, redacted where required;
- effective-permission evidence for the service identity;
- evidence of non-interactive service use and absence of human-account reuse;
- safe revoke/disable result;
- audit evidence distinguishing human and service activity;
- reviewer, timestamp and restricted evidence location.

## Acceptance

Set `checks.human_service_account_separation.result` to `PASS` only when all validation points above succeed on the approved staging deployment. The check must carry a non-empty evidence reference and the manifest must remain `phase8_2_pass: false` and `phase8_pass: false` during step-scoped validation.

Validate with:

```bash
python3 tools/phase8_platform_validation.py <manifest.json> --check human_service_account_separation
```

A repository test, local Compose run, emulator result or synthetic fixture must never be represented as external staging acceptance.
