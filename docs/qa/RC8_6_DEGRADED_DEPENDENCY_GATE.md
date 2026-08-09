# RC8.6 Degraded Dependency Performance/Correctness Gate

## Objective

Prove, with independently observable exact-head CI evidence, that DTMO preserves correctness and fail-closed publication governance while a representative downstream internal dependency is temporarily unavailable.

## Representative fault

- Dependency: `opensearch-index-sink`.
- Fault model: temporary unavailability injected in-process.
- Data: synthetic only.
- Accepted workload contract: `config/performance/phase5_workload_profile.json`.

This gate is intentionally bounded. It does **not** claim production OpenSearch security hardening, staging acceptance or the independent representative load/stress gate tracked in issue #1.

## Required evidence

The exact PR head must execute successfully:

1. `backend/tests/test_rc8_degraded_dependency_performance.py`;
2. `.github/workflows/degraded-dependency-performance.yml`;
3. every existing required RC4/RC6/RC7/RC8/open-source-governance regression workflow.

The retained artifact must contain JUnit results plus machine-readable degraded-dependency evidence showing outage observation, submitted/delivered counts, buffering/retry activity, data-loss/duplicate counts, recovery duration, provenance/non-publication invariants and explicit external-gate boundaries.

## Acceptance criteria

`PASS` requires all of the following on the exact head:

- dependency unavailability actually observed;
- delivered records equal submitted records;
- data loss = 0;
- duplicate candidate deliveries = 0;
- at least one record buffered/retried during outage;
- recovery <= accepted Phase-5 recovery budget;
- provenance preserved;
- `publish_approved=false` preserved;
- synthetic-only/privacy constraints preserved;
- dedicated workflow succeeds and retained evidence is inspectable;
- all other required regression workflows succeed.

## First exact-head execution

Superseded PR head `fd5739d7ae03a7e8574282afc39c3a0c83a205b8` registered 18 workflows.

Dedicated RC8.6 run `31289553204` succeeded. Artifact `9030943239`, digest `sha256:9de7af1dfe2eb6666601152b0452607e3a427af5224f4b33d59eed777eeeb39f`, was independently inspected and contained:

- 100 submitted / 100 delivered;
- 20 buffered during outage;
- 298 dependency-failure/retry events;
- dependency unavailability observed;
- 0 data loss;
- 0 duplicate candidate deliveries;
- 0.25 s injected outage;
- 1.013 s recovery against a 900 s budget;
- provenance preserved;
- publication state preserved;
- JUnit 6 tests, 0 failures/errors/skips.

The overall RC4 Quality Gate nevertheless failed because Ruff reported `F841` for an unused local `dependency_name` variable. That failure blocks acceptance and caused later type-check/full-test steps in that job to be skipped.

The first deterministic failure was remediated by removing the unused variable in commit `682a876a4339485ac1ee3708deaeef0ca70c0f65`. Subsequent documentation commits also change exact-head identity, so all superseded evidence is retained only as diagnostic history and cannot be used to mark the final head PASS.

## Fail-closed rule

Any absent, queued, cancelled, failed or unexecuted required workflow is **not PASS**. Missing or uninspectable retained evidence is **not PASS**. A test that never observes dependency unavailability is **not PASS**. Evidence from an older head is not acceptance evidence for a newer head.

## Current status

`CI_VALIDATION_PENDING` for RUN-20260809-084 after deterministic lint remediation and audit documentation update. Acceptance is deferred until the final exact head executes all required workflows successfully and the new retained artifact is independently inspected.
