# RC8.4 Ingestion Throughput Performance Gate

Status: `CI_VALIDATION_PENDING`

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

## Harness behavior

The bounded CI harness sends a unique synthetic record set through the production governance normalization function. A second identical pass uses the same replay registry and must yield replay quarantine for every item with zero additional candidates. Evidence records submitted, accepted, quarantined, replayed, duplicate-candidate and data-loss counts, achieved throughput, governance state and the final decision.

The default five-second CI run submits 500 records at the accepted sustained target. This is a scaled internal fixture and does not satisfy the external representative load/stress gate.

## Fail-closed rule

RC8.4 may only become `PASS` after the exact PR head has completed every required RC4/RC6/RC7/RC8 workflow successfully and the retained `ingestion-performance-evidence` artifact has been independently inspected. Missing, queued, cancelled or unexecuted CI is not PASS.

Any data loss, duplicate candidate creation, provenance loss, publication-state mutation, privacy-policy violation or failure to meet the sustained throughput budget fails the gate.

## Governance invariants

Performance execution cannot review, share or publish intelligence. Candidate and quarantine states remain `publish_approved=false`; human review and independent share approval remain required outside the harness.

## External gate boundary

Issue #1's independent representative load/stress gate remains open. RC8.4 is an internal bounded CI control only.
