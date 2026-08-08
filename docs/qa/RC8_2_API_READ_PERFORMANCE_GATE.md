# RC8.2 API Read Performance Gate

Status: `PASS`

## Control objective

Execute a bounded, synthetic API-read performance test against the accepted RC8.1 workload profile without broadening this run into search, ingestion or degraded-dependency testing.

## Scope

- target: DTMO `/health` read endpoint served by the real FastAPI application process;
- target request rate: 100 requests/second from `config/performance/phase5_workload_profile.json`;
- bounded duration: 5 seconds;
- bounded request count: 500;
- concurrency ceiling: 50;
- acceptance budgets: p95 <= 300 ms, p99 <= 750 ms, error rate <= 1%;
- retained evidence: JSON latency/error/governance evidence, JUnit regressions and API server log.

## Governance invariants

The harness reads its security/privacy requirements from the accepted workload profile and fails closed if publication is permitted, human review is not mandatory, review/share approval separation is removed, synthetic-only fixture policy is removed, or production personal data becomes permitted.

Runtime evidence also requires the tested DTMO endpoint to report `publication_gate=human-approval-required` and `authentication=api-key-and-rbac`. Load execution never grants publication approval, does not use production personal data and does not exercise mutating review/share-approval routes.

## Accepted exact-head evidence

Exact PR head: `e8ab9132bab6da753087d4cc830bac6541eb99ff`.

All 13 required workflows completed successfully: RC4 Quality #357, RC6 OpenSearch Recovery #109, RC6 Multi-store Recovery #99, RC7 Connector State #45, RC7 Live Connector Canary #90, RC7 Connector Contract #61, RC7 Payload Provenance #52, RC7 Connector Replay #16, RC7 Connector Freshness #12, RC7 Connector Failure Isolation #8, RC7 Connector Retry #5, RC7 Connector Timeout #4 and RC8 API Read Performance #1.

Retained artifact:

- name: `api-read-performance-evidence`;
- artifact ID: `9022168980`;
- digest: `sha256:ca930454d8795be70844ba22befe2ff4420c8c7002289b2c97c979bd9f889d30`;
- source workflow run: `31258791875` (`RC8 API Read Performance Gate` #1).

Independent artifact inspection confirmed:

- aggregate `decision=pass`;
- 500 total requests, 500 successful, 0 failed;
- achieved throughput `100.142` requests/second;
- error rate `0.0%` against maximum `1.0%`;
- p50 `1.636 ms`, p95 `1.878 ms`, p99 `11.059 ms`, maximum `14.67 ms`;
- accepted p95 budget `300 ms` and p99 budget `750 ms`;
- `authentication_boundary_reported=true`;
- `publication_gate_preserved=true`;
- `load_test_may_publish=false`;
- JUnit: 6 tests, 0 failures, 0 errors, 0 skips;
- API server log confirms successful HTTP 200 execution against the real FastAPI process.

PR #39 was merged with expected-head protection as `13fdadcfa83170b64713f3e72f7261501829e585`.

## External assurance boundary

This CI harness is an internal bounded performance control. It does not close issue #1's independent representative load/stress test gate and does not establish production-scale search, ingestion, queue-pressure or degraded-dependency capacity.

## Current decision

`PASS` for RC8.2 on the exact accepted head and retained artifact above. Phase 5 remains `IN PROGRESS`.

## Exactly one next priority

Implement a bounded synthetic OpenSearch/search-read performance harness driven by the accepted RC8.1 workload profile, with retained exact-head latency/error evidence and fail-closed governance checks. Ingestion, queue pressure, connector bursts and degraded dependencies remain outside that next run.
