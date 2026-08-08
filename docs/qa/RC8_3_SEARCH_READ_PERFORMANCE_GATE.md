# RC8.3 OpenSearch Search Read Performance Gate

Status: `PASS`

## Control objective

Execute a bounded, synthetic search-read performance test against a real OpenSearch service using the accepted RC8.1 search traffic and latency/error budgets, while proving search results retain provenance and cannot silently become publication-approved.

## Accepted scope

- OpenSearch service: 2.19.6 isolated CI service;
- CI corpus: 5,000 generated synthetic documents;
- target search rate: 40 requests/second;
- bounded duration: 5 seconds;
- bounded request count: 200;
- concurrency ceiling: 20;
- acceptance budgets: p95 <= 800 ms, p99 <= 1,500 ms, error rate <= 1%;
- retained evidence: JSON performance result, JUnit regressions, OpenSearch node/cluster/index metadata.

## Exact-head evidence

Accepted PR head: `78da9e8bc6ca6799bc6cf48d21ac79054bc9e8ae`.

All 14 required exact-head workflows completed successfully, including RC4 Quality #364, RC6 OpenSearch #116, RC6 Multi-store #106, all required RC7 connector regressions, RC8 API Read Performance #4 and RC8 OpenSearch Search Read Performance #3.

RC8 search workflow run: `31263541925`.

Retained artifact:

- name: `search-read-performance-evidence`;
- artifact ID: `9023474648`;
- digest: `sha256:06b4f0c6bf7273f7e4a2c5967c5e0e0445315b6282588503791209bbae1c939f`;
- retention: 30 days;
- exact head: `78da9e8bc6ca6799bc6cf48d21ac79054bc9e8ae`.

## Measured result

- decision: `pass`;
- 200 total requests;
- 200 successful requests;
- 0 failed requests;
- achieved rate: 40.161 requests/second;
- error rate: 0.0%;
- p50 latency: 4.528 ms;
- p95 latency: 7.700 ms;
- p99 latency: 12.131 ms;
- maximum latency: 40.517 ms.

The accepted budgets were p95 <= 800 ms, p99 <= 1,500 ms and error rate <= 1.0%.

## Integrity and governance invariants

Executed evidence confirmed:

- fixture class `synthetic-performance`;
- each search document retained required provenance;
- `provenance_preserved=true`;
- `publication_state_preserved=true`;
- `load_test_may_publish=false`;
- synthetic records remained `publish_approved=false`;
- performance execution did not approve, review or share intelligence;
- no production personal data or production secrets were used.

## Scaled-fixture and external boundary

The CI corpus is intentionally smaller than the RC8.1 representative target of 1,000,000 intelligence records. Evidence records `documents_loaded=5000`, `representative_intelligence_records_target=1000000` and `scaled_ci_fixture=true`.

The evidence also explicitly records `external_load_gate_satisfied=false`. This internal gate therefore does not close issue #1's independent representative load/stress gate.

The isolated CI service ran with the OpenSearch Security plugin disabled. Consequently, RC8.3 does not satisfy the separate production OpenSearch-hardening gate in issue #1.

## Merge decision

PR #40 was merged from the exact validated head with expected-head protection as `635a9736f9cb3b5091f00b99fc89eb47574858ae`.

## Exactly one next priority

Implement a bounded synthetic ingestion-throughput performance harness driven by the accepted RC8.1 profile, measuring sustained ingestion correctness and throughput with zero data loss and zero duplicate candidate creation. Queue pressure, connector bursts and degraded-dependency testing remain outside that next objective.