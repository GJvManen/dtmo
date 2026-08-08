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

## Historical evidence

Original RC8.5 head `0742af8ea56299034acae20bd742e3574ae678e8` passed its 16 workflows and retained artifact `9026316970` showed 250/250 accepted, 170 backpressure events, zero loss, zero duplicate candidates and 0.602 s recovery with provenance/non-publication preserved. That evidence is historical only after branch reconciliation and cannot be reused as exact-head acceptance.

## Current decision

`CI_VALIDATION_PENDING` for the reconciled PR #42 head created in RUN-20260809-082. Missing, queued or unexecuted CI is not PASS.
