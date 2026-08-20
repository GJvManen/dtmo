# Phase 11.10 Production-Equivalent Validation Gate

## Objective

Phase 11.10 validates the materially changed integrated Phase 11 candidate in an approved production-equivalent environment. Acceptance is candidate-bound and requires one immutable integrated deployment identity across all evidence classes.

**Status:** `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`

## Entry criteria

Before execution, record:

- production-equivalent environment identifier;
- accountable owner, validation operator and security/release reviewer;
- exact deployed Git commit;
- immutable application and supporting image digests;
- expected migration head;
- deployment/GitOps revision;
- exact approved prior immutable application digest for rollback.

The candidate fingerprint must be calculated from stable identity material before evidence is accepted. Missing or ambiguous identity blocks the exercise.

## Required evidence

The acceptance package must contain fresh evidence for:

1. immutable candidate identity;
2. migration/compatibility;
3. upgrade;
4. rollback;
5. health/readiness;
6. saturation/capacity;
7. recovery/continuity.

Each evidence item must identify the same candidate fingerprint and production-equivalent environment. Missing, placeholder, ambiguous, mixed-candidate, inaccessible or historical-only evidence fails closed.

Historical Phase 8/9 evidence is retained for audit history but is not reusable as Phase 11.10 acceptance evidence. Repository CI may validate the evidence contract and exact-head metadata, but it does not prove that a production-equivalent environment was deployed or exercised.

## Required operator sequence

1. Record and verify immutable candidate/environment identity.
2. Perform forward migration and verify application/schema compatibility.
3. Exercise upgrade from the exact approved prior digest to the candidate digest.
4. Capture post-upgrade health/readiness and representative functionality evidence.
5. Exercise the approved saturation/capacity workload and capture operational observations.
6. Exercise the selected recovery/continuity path with data-integrity and RPO/RTO observations where applicable.
7. Roll back the application to the exact prior immutable digest without automatic database down migration.
8. Capture post-rollback health/readiness and representative read/write evidence.
9. Reconcile every artifact to the same candidate fingerprint and environment.
10. Review release-blocking findings, deviations and residual risk.
11. Validate the evidence manifest and manually review each referenced external artifact.
12. Record the accountable owner decision.

## Repository execution package

- `docs/operations/PHASE11_10_PRODUCTION_EQUIVALENT_VALIDATION_RUNBOOK.md` — accountable execution procedure.
- `docs/evidence/PHASE11_10_PRODUCTION_EQUIVALENT_EVIDENCE.template.json` — manifest template; intentionally invalid while placeholders remain.
- `tools/phase11_production_equivalent_validation.py` — candidate fingerprint calculation and fail-closed manifest validation.
- `backend/tests/test_phase11_10_production_equivalent_validation.py` — repository contract and negative-case coverage.
- `.github/workflows/phase11-production-equivalent-validation.yml` — exact-head repository contract gate.
- `docs/evidence/EVIDENCE_INDEX.md` — evidence-class and claim-boundary index.

## Validator boundary

The validator verifies metadata consistency, required evidence classes, immutable identities, candidate fingerprint binding, rollback target, post-rollback health, timestamps, accountable review fields, deviation disposition and explicit claim boundaries.

The validator rejects references that identify only historical Phase 8/9 records, repository CI, synthetic fixtures, staging emulators or localhost observations. It also rejects a mutable or malformed image identity, mixed candidate fingerprints and incomplete review data.

A validator `PASS` is **not** proof that referenced external observations are true. The accountable reviewer must inspect the evidence itself.

## Fail-closed conditions

Phase 11.10 cannot be accepted when any of the following applies:

- required identity fields are missing or placeholders;
- the candidate/prior application identity is not an immutable `sha256:` digest;
- required evidence class is absent or not `PASS`;
- evidence classes use different candidate fingerprints;
- rollback does not restore the exact prior immutable application digest;
- post-rollback health is missing or failed;
- application rollback automatically down-migrates the database;
- saturation workload profile is not attributable;
- recovery evidence lacks required integrity/RPO/RTO observations where applicable;
- release-blocking findings remain open;
- deviations lack accountable disposition;
- observer/reviewer/timestamp/evidence attribution is incomplete;
- external evidence is historical-only, synthetic-only or inaccessible.

## Acceptance boundary

Phase 11.10 remains `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` until accountable environment execution supplies and reviews the complete fresh evidence set. It may be marked `PASS / OWNER_ACCEPTED` only after explicit accountable acceptance of that complete package.

Repository-green status alone does not complete Phase 11.10 and does not authorize production. Phase 11.11 independent external assurance is `NOT STARTED` and must use the same immutable integrated candidate accepted here. Phase 12 is `NOT STARTED`.
