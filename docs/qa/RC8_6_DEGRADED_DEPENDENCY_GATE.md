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

## Superseded first execution

Superseded PR head `fd5739d7ae03a7e8574282afc39c3a0c83a205b8` produced technically successful dedicated evidence but was correctly blocked by RC4 Quality due to Ruff `F841`. The deterministic lint defect was removed; evidence from that older head is retained only as diagnostic history.

## Final exact-head acceptance

Final PR #45 head: `e3c157505f4619ef2accbd1e2990fdc673c1cf86`.

All 18 registered required workflows completed with `success`, including:

- RC4 Quality Gate;
- both RC6 recovery gates;
- all RC7 connector, provenance, retry, timeout and failure-isolation gates;
- RC8 API-read, OpenSearch search-read, ingestion-throughput and queue-burst regression gates;
- Open Source Governance Gate;
- `RC8 Degraded Dependency Performance Gate` run `31289663568`.

Retained artifact `9030972060`, digest `sha256:f8ca3ccaac5b3bfb5ad9fbc30004d02f45b57ea6c84f4a7f33899178f160abbf`, was independently inspected and records:

- 100 submitted / 100 delivered;
- 20 buffered during a 0.25 s injected outage;
- 300 dependency-failure events;
- dependency unavailability observed;
- 0 data loss;
- 0 duplicate candidate deliveries;
- 1.013 s recovery against a 900 s budget;
- provenance preserved;
- publication state preserved;
- `load_test_may_publish=false`;
- `external_load_gate_satisfied=false`;
- `production_opensearch_hardening_satisfied=false`;
- JUnit 6 tests, 0 failures, 0 errors and 0 skipped.

PR #45 was merged with expected-head protection as `fc42e76e60783bdf1670fe2e208ef9eff70e68bc`.

## Fail-closed rule

Any absent, queued, cancelled, failed or unexecuted required workflow is **not PASS**. Missing or uninspectable retained evidence is **not PASS**. A test that never observes dependency unavailability is **not PASS**. Evidence from an older head is not acceptance evidence for a newer head.

## Current status

`PASS` via RUN-20260809-085. RC8.6 proves only the bounded synthetic degraded-dependency gate. The independent representative production load/stress test, production OpenSearch hardening, staging acceptance and later roadmap phases remain open.
