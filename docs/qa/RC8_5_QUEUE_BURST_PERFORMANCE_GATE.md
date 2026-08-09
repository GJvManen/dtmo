# RC8.5 Queue Burst Performance Gate

## Scope

This gate covers only bounded synthetic queue pressure and connector burst behavior driven by the accepted RC8.1 workload profile.

## Acceptance criteria

- burst input: 250 records/s scaled CI fixture;
- connector parallelism: 20;
- bounded queue must demonstrate observable backpressure;
- queue recovery after producer completion <= 900 seconds;
- data loss = 0;
- duplicate candidate creation = 0;
- provenance retained;
- all candidates remain `publish_approved=false`;
- synthetic-only data;
- all required exact-head GitHub Actions succeed;
- retained JSON and JUnit evidence independently inspected.

## Explicit exclusions

This gate does not satisfy the independent representative production load/stress gate in issue #1 and does not test degraded dependencies. Evidence must continue to state `external_load_gate_satisfied=false` and `degraded_dependency_tested=false`.

## Accepted evidence

PR #42 exact head `65c7949624c3770ce91d00c34a957b6b2cb9946a` completed all 17 registered required workflows with conclusion `success`.

Retained artifact `9029584698`, digest `sha256:a934d6179f347e3bf9a198fcb155e7996c42fc670959c2cfd50453969969b974`, was independently inspected and recorded:

- 250 submitted / 250 accepted;
- 170 observable backpressure events;
- queue depth 40 / capacity 40;
- 0 data-loss records;
- 0 duplicate candidate records;
- 0 quarantined records;
- recovery 0.602 seconds after producer completion;
- provenance preserved = true;
- publication state preserved = true;
- load test may publish = false;
- `external_load_gate_satisfied=false`;
- `degraded_dependency_tested=false`.

JUnit: 6 tests, 0 failures, 0 errors, 0 skipped.

PR #42 was merged with expected-head protection as `37a897aa39e33353c63f7b96192f06e61e200cdb`.

## Current decision

`PASS` for RC8.5 only. Phase 5 remains `IN PROGRESS` pending degraded-dependency correctness/capacity completion and the separately tracked independent external load/stress gate.
