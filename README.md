# DTMO

**Dutch Threat Monitoring for Education**

DTMO is an open, education-focused Cyber Threat Intelligence platform for historical incidents, current intelligence, vulnerabilities, indicators, supplier risk and management reporting.

## Current production-readiness status — 2026-08-11

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

The repository-controlled RC11 source-framework programme and RC12 unified-console/dashboard programme are accepted through PR #147. The current operational vendor catalog is connected through governed adapters, source administration and execution are available in the canonical console, and Grafana Operations/Intelligence dashboards are embedded through the managed same-origin `/grafana/` path. These repository-controlled results do not satisfy the external Phase 8, Phase 9 or Phase 10 gates.

## 16.0.0rc12 unified console

After `docker compose up --build`, open:

- `http://localhost:8000/` — canonical DTMO unified console;
- `http://localhost:8000/ui/console` — canonical console alias;
- `http://localhost:8000/grafana/` — managed same-origin Grafana path used by the console;
- `http://localhost:8000/docs` — OpenAPI/Swagger;
- `http://localhost:8000/health` — health status;
- `http://localhost:8000/metrics` — raw Prometheus metrics.

The unified console contains the governed source catalog and operations flow, administration controls, intelligence investigation, operational/intelligence analytics and read-only governance views without collapsing authority boundaries. Legacy `/ui/*` routes may remain for compatibility, but they are not separate product shells.

The source connection contract distinguishes catalogued, registered, enabled, executable, ingested, reviewed and share-approved states. All currently catalogued operational vendor feeds are connected through accepted built-in or framework adapters; research-reference sources remain deliberately non-executable where appropriate. Credential values are not stored in the catalog or registry.

Grafana uses dedicated least-privilege data access. Anonymous Grafana access remains disabled, the intelligence datasource is restricted to explicit reporting views, and the browser-facing console uses same-origin `/grafana/...` embeds rather than a direct `:3000` target. Native accessible chart/table fallbacks remain available in the DTMO console.

Existing server-side RBAC remains authoritative. Search, ingestion, administration and dashboard access do not grant review or publication authority. Review and external share approval remain distinct human decisions and self-approval remains prohibited.

For OpenSearch 2.12+ local Compose bootstrap requires `OPENSEARCH_INITIAL_ADMIN_PASSWORD` in `.env`. Real credentials, AIStor license material and image digests must remain outside source control.

## Documentation

Start with [`docs/README.md`](docs/README.md).

Key documents:

- [Current project state](docs/project/CURRENT_STATE.md)
- [Executive status](docs/project/EXECUTIVE_STATUS.md)
- [Production roadmap](docs/roadmap/PRODUCTION_ROADMAP.md)
- [Source connection matrix](docs/qa/SOURCE_CONNECTION_MATRIX.md)
- [RC12 programme completion gate](docs/qa/RC12_6_UNIFIED_CONSOLE_COMPLETION_GATE.md)
- [16.0.0rc12 release notes](docs/releases/16.0.0rc12.md)
- [Development run log](docs/development/RUN_LOG.md)
- [Evidence index](docs/evidence/EVIDENCE_INDEX.md)
- [Traceability matrix](docs/traceability/TRACEABILITY_MATRIX.md)
- [System architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Security overview](docs/security/SECURITY_OVERVIEW.md)
- [Operations manual](docs/operations/OPERATIONS_MANUAL.md)

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

Then open `http://localhost:8000/`.

## Open source

DTMO is licensed under the **Apache License, Version 2.0** (`Apache-2.0`). See `LICENSE`, `NOTICE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SUPPORTED_VERSIONS.md`, `docs/legal/LICENSING.md` and `docs/legal/THIRD_PARTY.md`.

## Exactly one next priority

Phase 8 real staging deployment parity: obtain one approved production-equivalent staging deployment and collect the complete ten-class evidence package against one immutable release/deployment identity. Repository emulator or local-container evidence must not be used as a substitute for that external acceptance evidence.
