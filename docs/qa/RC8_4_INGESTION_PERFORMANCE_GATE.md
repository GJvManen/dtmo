# RC8.4 Ingestion Throughput Performance Gate

Status: `PASS`

## Control objective

Prove that the governed DTMO ingestion normalization/replay path can process the accepted Phase 5 sustained synthetic workload without data loss or duplicate candidate creation, while retaining provenance and fail-closed publication governance.

## Accepted target contract

Source: `config/performance/phase5_workload_profile.json`.

- sustained ingestion: at least 100 records/s;
- maximum data loss: 0 records;
- maximum duplicate candidates: 0 records;
- maximum error rate: 1%;
- synthetic-only fixtures;
- production personal data forbidden;
- load execution may not publish;
- human review remains mandatory;
- share approval remains separate from review;
- service accounts may not approve sharing.

## Accepted exact-head evidence

PR #41 exact head: `d3ab690ea2b4144e21598f8c2d74ef55c6a066c6`.

All 15 required RC4/RC6/RC7/RC8 workflows completed successfully, including RC8 Ingestion Performance Gate #1 (run `31268483024`).

Retained artifact:

- name: `ingestion-performance-evidence`;
- artifact ID: `9024869189`;
- digest: `sha256:bf419775b1ae51df4970e8e1ecceb319ab2841a574559d93d557394a72623b06`;
- expired at acceptance: `false`.

Independent inspection confirmed:

- aggregate `decision=pass`;
- 500 submitted and 500 accepted candidates;
- 0 data-loss records;
- 0 duplicate candidate records;
- 0% error rate;
- achieved throughput 108081.257 records/s against the minimum 100 records/s budget;
- second identical pass produced 500 replayed records and no additional candidates;
- provenance preserved;
- publication state preserved;
- `load_test_may_publish=false`;
- `external_load_gate_satisfied=false`;
- 6 executed regression tests with 0 failures, 0 errors and 0 skips.

PR #41 was merged with expected-head protection as `781bc043da64fdeb7fc18c69f25521a2f7f22f91`.

## Fail-closed rule

Any data loss, duplicate candidate creation, provenance loss, publication-state mutation, privacy-policy violation or failure to meet the sustained throughput budget fails the gate. Missing, queued, cancelled or unexecuted CI is never PASS.

## Governance invariants

Performance execution cannot review, share or publish intelligence. Candidate and quarantine states remain `publish_approved=false`; human review and independent share approval remain required outside the harness.

## External gate boundary

Issue #1's independent representative load/stress gate remains open. RC8.4 is an internal bounded CI control only.
