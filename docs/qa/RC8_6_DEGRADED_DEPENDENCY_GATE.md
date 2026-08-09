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

The retained artifact must contain:

- JUnit results for the focused regressions;
- `degraded-dependency-performance-evidence.json`;
- explicit observation of dependency unavailability;
- submitted and delivered record counts;
- buffered-during-outage and dependency-failure counts;
- data-loss and duplicate-candidate counts;
- recovery duration;
- provenance and non-publication invariants;
- explicit external-gate boundaries.

## Acceptance criteria

`PASS` requires all of the following on the exact head:

- dependency unavailability was actually observed;
- delivered records equal submitted records;
- data loss = 0;
- duplicate candidate deliveries = 0;
- at least one record was buffered/retried during the outage;
- recovery <= accepted Phase-5 recovery budget;
- provenance preserved;
- `publish_approved=false` preserved;
- synthetic-only/privacy constraints preserved;
- dedicated workflow succeeds and retained evidence is inspectable;
- all other required regression workflows succeed.

## Fail-closed rule

Any absent, queued, cancelled, failed or unexecuted required workflow is **not PASS**. Missing or uninspectable retained evidence is **not PASS**. A test that never observes dependency unavailability is **not PASS**.

## Current status

`CI_VALIDATION_PENDING` for RUN-20260809-084. Acceptance is deferred until exact-head workflows execute and the retained artifact is independently inspected.
