# DTMO

**Dutch Threat Monitoring for Education**

DTMO is an open, education-focused Cyber Threat Intelligence platform for historical incidents, current intelligence, vulnerabilities, indicators, supplier risk and management reporting.

## Current production-readiness status — 2026-08-10

DTMO is **not production ready**.

| Phase | Status |
|---|---|
| 1. CI and workflow integrity | `PASS` |
| 2. Application security and identity | `PASS` internally |
| 3. Data integrity and recovery | `PASS` internally |
| 4. Connector reliability and provenance | `PASS` internally |
| 5. Performance and scalability | `PASS` internally |
| 6. Accessibility and operational UX | `BLOCKED_EXTERNAL` — genuine VoiceOver/NVDA evidence |
| 7. Observability and incident operations | `PASS` |
| 8. Staging acceptance | `BLOCKED_EXTERNAL` — real staging/deployment parity |
| 9. External assurance | `NOT COMPLETE`; readiness/intake contract accepted |
| 10. Production go/no-go | `NOT STARTED` |

PR #110 exact head `5549ac1f28307c8bfa8c2ea1bf39341bb33983a0` completed all 48 registered workflows successfully and merged as `0b9a6d51dcd6e4fa984888d172e1fb5f5d6d52f2`, making RUN-159's Phase 9 external-assurance intake baseline authoritative on `main`.

## Documentation

Start with [`docs/README.md`](docs/README.md).

Key documents:

- [Current project state](docs/project/CURRENT_STATE.md)
- [Executive status](docs/project/EXECUTIVE_STATUS.md)
- [Production readiness report](docs/project/PRODUCTION_READINESS_REPORT.md)
- [Production acceptance checklist](docs/project/PRODUCTION_CHECKLIST.md)
- [Production roadmap](docs/roadmap/PRODUCTION_ROADMAP.md)
- [Development run log](docs/development/RUN_LOG.md)
- [Evidence index](docs/evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](docs/traceability/TRACEABILITY_MATRIX.md)
- [System architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Security overview](docs/security/SECURITY_OVERVIEW.md)
- [Operations manual](docs/operations/OPERATIONS_MANUAL.md)
- [Lessons learned](docs/project/LESSONS_LEARNED.md)
- [ADR-001 — Evidence and claim boundaries](docs/project/ADR/ADR-001-EVIDENCE-CLAIM-BOUNDARIES.md)

Detailed gate decisions remain in `docs/qa/`; detailed PDCA evidence remains in `docs/development/runs/`.

## Governance invariants

- RBAC and least privilege;
- review and human share approval are separate decisions;
- separation of duties is preserved;
- service accounts/connectors/CI/staging access cannot grant publication authority;
- provenance and confidence are preserved;
- privacy and data minimization apply to logs and evidence;
- secret values, credentials and tokens are excluded from repository evidence;
- missing, queued, cancelled, skipped, failed, stale, inaccessible or inferred evidence is never `PASS`;
- successful connector, recovery, performance, CI, emulator or staging execution never automatically publishes or approves sharing.

## Phase 8 blocker

Real staging acceptance requires one approved immutable deployment identity with the complete ten-class deployment-parity package: environment/owner, reachable endpoint, deployed release/image identity, infrastructure/configuration parity, approved secret-manager/least-privilege identities, TLS/network restrictions, staging data/no-production-credential confirmation, deployment/change record, rollback target/procedure and deployment-time threat/CVE/vendor-advisory review.

Repository-controlled emulator configuration and bounded application-container runtime smoke are accepted only for their explicit scopes and do not satisfy this gate.

## Phase 9 external assurance

The accepted readiness contract requires independent evidence for penetration testing, representative load/stress, full backup/restoration, production platform hardening, secrets-management acceptance, operational/stakeholder acceptance and staging/production deployment acceptance.

No external assurance activity is considered complete without attributable, dated, reviewable evidence and findings disposition.

## Quick start

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
cp .env.example .env
docker compose up --build
```

Important endpoints in the local stack include API `:8000`, OpenAPI `/docs`, health `/health`, metrics `/metrics`, MinIO Console `:9001` and Prometheus `:9090`.

## Open source

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). See `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

## Exactly one next priority

Acquire the first missing independent assurance evidence class from issue #1 without treating absent external execution as PASS. In roadmap order this is the independent penetration test against an approved target deployment.
