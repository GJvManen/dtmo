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

PR #112 exact head `e5e0d5e808d1f66c8f512fa35bd0ea3932fe8631` completed all 48 registered workflows successfully and merged as `5c2a9c9a5d0d936784597899c97bf5be253c2394`. Release candidate **16.0.0rc6** is therefore the accepted repository-controlled professional frontend baseline. This does not close genuine VoiceOver/NVDA, real staging, external-assurance or production go/no-go gates.

## 16.0.0rc6 Threat Operations Console

After `docker compose up --build`, open:

- `http://localhost:8000/` — DTMO Threat Operations Console;
- `http://localhost:8000/ui/analyst-search` — focused Analyst workspace;
- `http://localhost:8000/ui/share-approval` — governed Share Approval workspace;
- `http://localhost:8000/ui/auditor` — read-only Auditor workspace;
- `http://localhost:8000/ui/ciso-security` — CISO Security workspace;
- `http://localhost:8000/docs` — OpenAPI/Swagger;
- `http://localhost:8000/health` — health status;
- `http://localhost:8000/metrics` — Prometheus metrics;
- `http://localhost:9001/` — AIStor/MinIO console;
- `http://localhost:9090/` — Prometheus.

The rc6 console is organized around five operator tasks: **Overview, Intelligence, Governance, Audit and Security**. It adds persistent navigation, clear status/KPI cards, professional search/results, explicit review/share decision steps, a read-only audit table, isolated privileged security actions, responsive mobile/tablet behavior and a shared design system across all role-specific views.

Browser-side local/dev/staging test identity material is stored only in per-tab `sessionStorage`; production authentication remains the configured bearer-token/identity-provider path. Client-side permission presentation is UX only: server-side RBAC remains authoritative. Review and external share approval remain separate human decisions and self-approval remains prohibited.

For OpenSearch 2.12+ the local Compose bootstrap requires `OPENSEARCH_INITIAL_ADMIN_PASSWORD` in `.env`. Real credentials, AIStor license material and image digests must remain outside source control.

## Documentation

Start with [`docs/README.md`](docs/README.md).

Key documents:

- [Current project state](docs/project/CURRENT_STATE.md)
- [Executive status](docs/project/EXECUTIVE_STATUS.md)
- [Production readiness report](docs/project/PRODUCTION_READINESS_REPORT.md)
- [Production acceptance checklist](docs/project/PRODUCTION_CHECKLIST.md)
- [Production roadmap](docs/roadmap/PRODUCTION_ROADMAP.md)
- [Development run log](docs/development/RUN_LOG.md)
- [Frontend UX architecture](docs/ux/FRONTEND_UX.md)
- [Frontend UX release gate](docs/qa/FRONTEND_UX_RELEASE_GATE.md)
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
# Replace all placeholders in .env with local secret values/references.
docker compose up --build
```

Then open `http://localhost:8000/` for the DTMO Threat Operations Console.

## Open source

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). See `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

## Exactly one next priority

Acquire and validate one approved real staging deployment plus the complete ten-class deployment-parity evidence package for Phase 8. Keep the gate `BLOCKED_EXTERNAL` until independently reviewable evidence exists for one immutable staged release.