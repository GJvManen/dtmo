# RC8.1 Performance Workload Profile Gate

Status: `PASS`

## Control objective

Establish one reviewable, machine-readable workload contract for Phase 5 before any load generation is implemented. The contract defines representative synthetic education-sector CTI volumes, traffic rates, latency/throughput/resource budgets, integrity constraints and governance invariants.

## Accepted exact-head evidence

PR #38 exact head `9e45a0e1f8991d42c841ebfa4e03b42fe64d4dbb` completed all 12 required pull-request workflows successfully:

- RC4 Quality Gate #352;
- RC6 OpenSearch Recovery Gate #104;
- RC6 Multi-store Recovery Gate #94;
- RC7 Connector State Gate #44;
- RC7 Live Connector Canary Gate #85;
- RC7 Connector Contract Gate #56;
- RC7 Payload Provenance Gate #47;
- RC7 Connector Replay Gate #15;
- RC7 Connector Freshness Gate #11;
- RC7 Connector Failure Isolation Gate #7;
- RC7 Connector Retry Gate #4;
- RC7 Connector Timeout Gate #3.

PR #38 was merged with expected-head protection as squash commit `67ff969554fbced6b2efbd0e84b7d050bd16c3cc`.

No configured-only, queued, skipped, absent or unexecuted workflow was interpreted as PASS.

## Defined budgets

The accepted profile defines 1,000,000 intelligence records, 500,000 vulnerabilities, 5,000,000 IOCs, 20,000,000 graph edges and 500 GiB raw-evidence capacity. Representative traffic includes 100 API reads/s, 40 searches/s, 100 records/s sustained ingestion and a 250 records/s ten-minute burst.

Primary target budgets are API-read p95 <= 300 ms / p99 <= 750 ms, search p95 <= 800 ms / p99 <= 1,500 ms, dashboard p95 <= 1,500 ms, error rate <= 1%, zero data loss and zero duplicate candidate creation.

These remain acceptance targets, not measured performance results.

## Governance invariants

- only synthetic or approved public fixtures are permitted;
- production personal data is forbidden in performance fixtures;
- RBAC remains active under load;
- human review remains mandatory;
- share approval remains separate from review;
- service accounts may not approve sharing;
- performance or ingestion success never implies publication approval;
- provenance and integrity must survive burst and degraded-dependency scenarios.

## Current decision

RC8.1 is `PASS`. Phase 5 remains `IN PROGRESS`; representative performance execution has not yet been performed, and the external load/stress gate in issue #1 remains open.

## Exactly one next priority

Implement a bounded synthetic API/read performance harness against this accepted profile, producing machine-readable latency/error evidence and fail-closed acceptance evaluation. Do not add search, ingestion or degraded-dependency load in the same run.
