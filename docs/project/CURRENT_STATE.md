# DTMO Current Project State

Last reconciled: 2026-08-10 — RUN-20260810-155 (`CI_VALIDATION_PENDING`; staging-emulator runtime-smoke fresh-base remediation)

## Executive status

- Phase 1 — CI/workflow integrity: `PASS`.
- Phase 2 — application security and identity: `PASS` for internal roadmap gates.
- Phase 3 — data integrity and recovery: `PASS` for internal roadmap gates.
- Phase 4 — connector reliability and provenance: `PASS` for internal roadmap gates.
- Phase 5 — performance and scalability: `PASS` for internal roadmap gates.
- Phase 6 — frontend accessibility and operational UX: `BLOCKED_EXTERNAL` only for genuine VoiceOver/NVDA behavior.
- Phase 7 — observability and incident operations: `PASS`.
- Phase 8 — staging acceptance: `BLOCKED_EXTERNAL` for a real staging deployment and the ten deployment-parity evidence classes. The repository-controlled staging-emulator configuration contract is accepted as `PASS`; the bounded application-container runtime-smoke extension is `CI_VALIDATION_PENDING` on RUN-155.
- Phase 9 — external assurance: `NOT COMPLETE`.
- Phase 10 — production go/no-go: `NOT STARTED`.

DTMO is **not production ready**. Issue #1 remains authoritative for remaining external production-acceptance gates.

## Accepted staging-emulator baseline

PR #104 final exact head `93d1a659b7b136546ffcf73102890f5d2d00ba84` completed 47/47 workflows successfully. Retained artifact `9045039742`, digest `sha256:959586b389579dfd37bda60eecdfb67e0251eaf4a78daed214986cefe771ce65`, is exact-head bound with decision `pass` and JUnit 4/4. The emulator proves configuration/topology only, not real staging or dependency runtime parity.

PR #106 final exact head `ff0a490e46c2f9529441d8a5294030af498dbe14` completed 47/47 workflows successfully after RUN-154 repaired the stale lifecycle-state regression. PR #106 merged as `b57a6daa775d2f1f88a2d1b67b191da757fa743f`, so RUN-153/RUN-154 documentation reconciliation is accepted.

## RUN-155 runtime-smoke remediation

An already-open parallel PR #105 attempted the next bounded Phase 8 objective: execute the exact-head DTMO application container in production configuration mode with loopback-only exposure, read-only root filesystem, tmpfs, no-new-privileges, dropped capabilities, disabled live connectors/AI analyst, preserved human publication/share approval, and privacy-safe runtime evidence.

PR #105 exact head `51607417c6bc3c64c5bb9fbc1221a0e1e0e48ba2` succeeded in the dedicated `Phase 8 Staging Emulator Runtime Gate`, but RC4 failed at Ruff S310 before type-check/tests. The branch also became stale/conflicted against `main` after PR #106 merged.

RUN-155 therefore ports that bounded runtime-smoke work onto current `main` and strengthens the helper with executable URL validation: only `http` requests to `127.0.0.1` or `localhost` are accepted before request construction. Fresh complete exact-head CI and retained runtime evidence are required before the gate can be accepted.

## Phase 8 claim boundary and remaining blocker

The runtime-smoke extension, even if accepted, does not execute the complete dependency topology or external TLS gateway and does not prove a real staging environment. Real environment evidence must still establish environment identity/owner, reachable endpoint, immutable deployed digests/release, infrastructure/config parity, approved secrets/identity references, TLS/network restrictions, data-class/no-production-credential confirmation, deployment change record, rollback target, and deployment-time security/CVE/vendor-advisory review.

## Security and governance invariants

RBAC, separation of duties, privacy, provenance, auditability and human share approval remain unchanged. Emulator or staging access cannot grant publication authority or human share approval. Missing, stale, inaccessible or inferred environment evidence is never `PASS`.

## Exactly one current priority

Verify every registered workflow on the RUN-155 exact final PR head and independently inspect retained `phase8-staging-emulator-runtime-evidence`. Merge only on complete success.
