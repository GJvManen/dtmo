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
| 6. Accessibility and operational UX | internal browser gates accepted; genuine VoiceOver/NVDA `BLOCKED_EXTERNAL` |
| 7. Observability and incident operations | `PASS` internally |
| 8. Staging acceptance | `BLOCKED_EXTERNAL` — real staging/deployment parity |
| 9. External assurance | `NOT COMPLETE` |
| 10. Production go/no-go | `NOT STARTED` |

RC10.1 / PR #116 is accepted: exact head `d41d9e60a4a67ddb30345eecee4042d1c19a6cf5` completed every registered workflow and merged as `b000ef2275d52ff098d2d2bd8df76136cea3b051`. RUN-20260810-176 / RC10.2 is the current bounded objective and remains `CI_VALIDATION_PENDING` until its own final exact head is fully green.

## 16.0.0rc10 Operations Workspace

After `docker compose up --build`, open:

- `http://localhost:8000/ui/operations` — unified Security Operations Workspace;
- `http://localhost:8000/` — Threat Operations Console;
- `http://localhost:8000/ui/admin-sources` — governed Source Registry;
- `http://localhost:8000/ui/analyst-search` — Analyst workspace;
- `http://localhost:8000/ui/share-approval` — Share Approval workspace;
- `http://localhost:8000/ui/auditor` — read-only Auditor workspace;
- `http://localhost:8000/ui/ciso-security` — CISO Security workspace;
- `http://localhost:8000/docs` — OpenAPI/Swagger;
- `http://localhost:8000/health` — health status;
- `http://localhost:8000/metrics` — raw Prometheus metrics;
- `http://localhost:8000/api/v1/operations/summary` — bounded aggregate operational telemetry;
- `http://localhost:9001/` — AIStor/MinIO console;
- `http://localhost:9090/` — Prometheus.

RC10.1 established the professional operations shell with consolidated navigation, command palette, notification drawer and workspace tabs. RC10.2 replaces the remaining synthetic dashboard placeholder with live read-only widgets backed by the existing Prometheus client registry. The browser receives only bounded aggregate values for request volume/latency/in-flight, queue backlog, connector runs, trace contexts and active API/connector/storage/search alerts; sensitive request dimensions and credentials are excluded.

Existing server-side RBAC remains authoritative. Review and external share approval remain distinct human decisions, self-approval remains prohibited, and operational telemetry never grants publication authority.

For OpenSearch 2.12+ the local Compose bootstrap requires `OPENSEARCH_INITIAL_ADMIN_PASSWORD` in `.env`. Real credentials, AIStor license material and image digests must remain outside source control.

## Documentation

Start with [`docs/README.md`](docs/README.md).

Key documents:

- [Current project state](docs/project/CURRENT_STATE.md)
- [Production roadmap](docs/roadmap/PRODUCTION_ROADMAP.md)
- [Development run log](docs/development/RUN_LOG.md)
- [RC10 release notes](docs/releases/16.0.0rc10.md)
- [RC10.2 Unified Operational Dashboards Gate](docs/qa/RC10_2_UNIFIED_DASHBOARDS_GATE.md)
- [RUN-176 RC10.2 dashboard implementation](docs/development/runs/RUN-20260810-176.md)
- [Evidence index](docs/evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](docs/traceability/TRACEABILITY_MATRIX.md)
- [System architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Security overview](docs/security/SECURITY_OVERVIEW.md)
- [Operations manual](docs/operations/OPERATIONS_MANUAL.md)

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

## External blockers

Real staging acceptance still requires one approved immutable deployment identity with the complete ten-class deployment-parity package. Genuine assistive-technology execution, independent penetration testing and remaining external assurance evidence are also still absent. Repository-controlled CI does not satisfy those external gates.

## Quick start

```bash
git clone https://github.com/GJvManen/dtmo.git
cd dtmo
cp .env.example .env
# Replace all placeholders in .env with local secret values/references.
docker compose up --build
```

Then open `http://localhost:8000/ui/operations` for the unified Operations Workspace.

## Open source

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). See `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

## Exactly one next priority

Complete exact-head CI validation for RUN-20260810-176 / RC10.2. Merge only on complete success. After acceptance, start RC10.3 Threat Intelligence Workspace; otherwise remediate only the first concrete failing root cause.
