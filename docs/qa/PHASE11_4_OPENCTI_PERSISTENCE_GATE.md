# Phase 11.4 OpenCTI Canonical Persistence Gate

Status: **IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED**  
Last updated: **2026-08-16**

## Objective

Accept the final bounded Phase 11.4 repository slice only when canonical OpenCTI mapping persistence, immutable reconciliation history, database-before-checkpoint ordering and professional documentation are synchronized and fully green on one exact PR head.

## Required engineering evidence

The exact head must prove:

- migration `0012_opencti_mapping_persistence` follows `0011_intelowl_enrichment_history`;
- current mapping state is keyed by explicit DTMO item, OpenCTI internal identity and STIX identity;
- conflicting OpenCTI/STIX identity drift fails closed;
- markings, confidence, timestamps, external references and provenance remain attributable;
- immutable revision snapshots are deduplicated by stable SHA-256 snapshot hash;
- unchanged replay is idempotent;
- database constraints enforce `external_share_authorized=false` and `local_compromise_proven=false`;
- PostgreSQL commit completes before `commit_page(page)` can advance the durable cursor;
- failed database commit leaves the checkpoint unchanged;
- replay after a database-commit/checkpoint-write interruption is safe;
- connector registration, MISP synchronization, external enrichment, TheHive case creation, publication and arbitrary OpenCTI mutation remain excluded;
- authoritative architecture/integration/security/operations/evidence/roadmap/README documentation is synchronized.

## Required tests and gates

- `backend/tests/test_phase11_4_opencti_adapter.py`;
- `backend/tests/test_phase11_4_opencti_persistence.py`;
- `backend/tests/test_opencti_integration_contract.py`;
- `backend/tests/test_professional_documentation_contract.py`;
- Phase 11 OpenCTI Integration Contract Gate;
- Professional Documentation Gate;
- RC4 Quality Gate and all other repository-required exact-head workflows.

## Fail-closed acceptance

Any failed, skipped where required, cancelled, queued, stale or inaccessible required exact-head evidence blocks merge. A newer commit invalidates evidence from an earlier head. Merge uses expected-head protection.

## Non-evidence

Repository acceptance does not prove live OpenCTI connectivity, deployed credentials/RBAC/markings, real STIX interoperability, production graph quality/performance, privacy approval, HA/recovery, production-equivalent validation, independent assurance or production authorization. Historical Phase 8/9 evidence remains candidate-bound.

## Completion rule

Only after this slice is protected-merged and lifecycle documentation is reconciled may Phase 11.4 be marked `PASS / REPOSITORY_COMPLETE`. The next bounded priority is then Phase 11.5 MISP consolidation.
