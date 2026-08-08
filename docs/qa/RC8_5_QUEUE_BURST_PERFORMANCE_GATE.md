# RC8.5 Queue Pressure and Connector Burst Performance Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Prove that DTMO can absorb a bounded connector-ingestion burst through explicit queue backpressure without losing records, creating duplicate candidates, discarding provenance or weakening publication governance, and that the queue returns to empty within the accepted recovery budget.

## Accepted workload contract

Source: `config/performance/phase5_workload_profile.json`.

- ingestion burst: 250 records/second;
- configured representative burst duration: 600 seconds;
- connector parallelism: 20;
- accepted sustained consumer reference rate: 100 records/second;
- maximum recovery after burst: 900 seconds;
- maximum data loss: 0 records;
- maximum duplicate candidates: 0 records.

The CI gate executes a one-second scaled burst fixture. This is deliberately smaller than the representative 600-second envelope and therefore cannot satisfy the independent external load/stress gate.

## Gate semantics

PASS requires all of the following in retained exact-head evidence:

- every submitted record is accepted or explicitly quarantined; for the clean synthetic fixture all records must be accepted;
- data loss is zero;
- duplicate candidate creation is zero;
- bounded queue depth never exceeds configured capacity;
- at least one real backpressure event occurs during the burst;
- queue recovery completes within 900 seconds;
- source URI, confidence, payload digest and raw synthetic evidence are preserved;
- every connector-controlled publication state remains `publish_approved=false`;
- focused regressions execute without failures, errors or skips;
- the dedicated aggregate workflow fails closed if the primary evidence job is missing or unsuccessful.

## Governance and privacy invariants

- fixtures are generated synthetic performance records only;
- production personal data is forbidden;
- performance execution cannot review intelligence, approve sharing or publish;
- human review remains mandatory and share approval remains separated from review;
- service accounts cannot approve sharing;
- performance success does not imply operational or production acceptance.

## Explicit exclusions

- degraded PostgreSQL, OpenSearch, object-storage or network dependencies;
- representative 600-second production-envelope load execution;
- external independent load/stress assurance;
- production capacity sign-off.

Evidence must therefore retain `external_load_gate_satisfied=false` and `degraded_dependency_tested=false`.

## Current decision

`CI_VALIDATION_PENDING`. Implementation and regression contracts are committed, but exact-head workflows and retained runtime evidence must execute before this gate can be marked PASS.
