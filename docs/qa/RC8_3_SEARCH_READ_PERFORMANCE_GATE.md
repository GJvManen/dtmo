# RC8.3 OpenSearch Search Read Performance Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Execute a bounded, synthetic search-read performance test against a real OpenSearch service using the accepted RC8.1 search traffic and latency/error budgets, while proving search results retain provenance and cannot silently become publication-approved.

## Scope

- OpenSearch service: 2.19.1 isolated CI service, matching the existing RC6 recovery topology;
- CI corpus: 5,000 generated synthetic documents;
- target search rate: 40 requests/second;
- bounded duration: 5 seconds;
- bounded request count: 200;
- concurrency ceiling: 20;
- acceptance budgets: p95 <= 800 ms, p99 <= 1,500 ms, error rate <= 1%;
- retained evidence: JSON performance result, JUnit regressions, OpenSearch node/cluster/index metadata.

## Integrity and governance invariants

- only generated synthetic documents are loaded;
- each hit must retain an external identifier and HTTPS source URI;
- every synthetic record carries `publish_approved=false`;
- any returned `publish_approved=true` causes fail-closed rejection;
- performance execution cannot approve, review or share intelligence;
- human review/share approval separation remains unchanged;
- no production personal data or production secrets are used.

## Scaled-fixture boundary

The CI corpus is intentionally smaller than the RC8.1 representative target of 1,000,000 intelligence records. Evidence records both cardinalities and marks the run as a scaled CI fixture. This internal gate does not prove production-scale search capacity and does not close issue #1's independent representative load/stress gate.

## Evidence rule

`PASS` requires actual exact-head execution of this dedicated workflow plus all required release-critical regression workflows, followed by independent inspection of the retained artifact. Missing, queued, skipped or unexecuted jobs are not PASS.

## Current decision

`CI_VALIDATION_PENDING` until exact-head GitHub Actions execute and retained evidence is inspected.

## Exactly one next priority

Inspect exact-head CI for RC8.3; remediate only the earliest deterministic failure, or accept/merge only if every required gate and retained search-read evidence succeeds.