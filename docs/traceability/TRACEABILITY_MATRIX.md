# DTMO Production Traceability Matrix

Last updated: **2026-08-12**

| Requirement area | Stage | Primary evidence | QA / evidence family | Current status | Remaining dependency |
|---|---:|---|---|---|---|
| CI integrity and regression protection | 1 | Exact-head workflow execution and protected merge | RC4 Quality / workflow contracts | `PASS` | Continue per-change exact-head discipline |
| RBAC, identity and least privilege | 2 | Security/identity tests, browser journeys, audit evidence | Security/RC9/Administration gates | `PASS` within accepted baseline | Real staging IAM validation + Phase 9 review |
| Human/service-account separation | 2 | Role/principal constraints and privileged-action tests | Security/Administration gates | `PASS` | Validate deployed identity model in Phase 8 |
| Review vs external-share separation | 2 | Separate permissions/actions and browser/API evidence | Security/governance gates | `PASS` | Preserve in staging/production |
| Data integrity and recovery | 3 | Migrations, storage/search recovery and integrity evidence | RC6 recovery / storage gates | `PASS` within repository boundary | Production-equivalent recovery evidence in later phases |
| Canonical PostgreSQL persistence | 3 / RC13 | Connector commit-before-success and console visibility evidence | RC13 Canonical Connector Commit Visibility | `PASS` | Revalidate in staging |
| Raw evidence retention | 3 / 4 | Object-storage/source provenance evidence | Storage / provenance gates | `PASS` | Revalidate staging storage identity/retention |
| Connector reliability | 4 | Contract/state/retry/timeout/replay/freshness evidence | RC7 connector gates | `PASS` | Deployed provider/runtime acceptance |
| Provenance and normalization | 4 / RC13 | Payload/source evidence and source-record normalization | RC7 provenance / RC13 normalization | `PASS` | Ongoing source governance |
| Performance/scalability | 5 | Ingestion/read/queue/concurrency evidence | RC8 performance gates | `PASS` within tested bounds | Representative Phase 9 external load/stress |
| Accessibility and browser UX | 6 / RC13 | Keyboard/contrast/reflow/browser journeys + owner acceptance | RC9 / RC13 browser gates | `PASS` | Preserve through enhancements and staging |
| Request observability | 7 | Correlation/trace evidence | RC10 request/trace gates | `PASS` | Staging operational validation |
| Alerting and dashboards | 7 | Queue/storage/API/search/connector alerting and dashboard evidence | RC10 alerting/dashboard gates | `PASS` | Staging notification/operational acceptance |
| Runbooks and exercises | 7 | Runbook and controlled exercise evidence | RC10 runbook gates | `PASS` | Environment-specific ownership/operations |
| Unified-console functionality | RC13 | Functional browser/integration evidence + accountable owner acceptance | RC13 Functional Console Acceptance | `PASS / OWNER_ACCEPTED` | Preserve baseline; reopen only on regression evidence |
| Source catalog and execution | RC13 | Catalog bootstrap, source execution and feedback | RC13 source gates | `PASS` | Staging validation; manual onboarding is enhancement |
| Native Visual Analytics | RC13 | Severity/source/connector/review browser evidence | RC13 Visual Analytics | `PASS` | Richer filtering/trends are enhancements |
| Governed Administration | RC13 | Principal/role assignment, safety and audit evidence | RC13 Administration RBAC | `PASS` | Richer role/permission UX is enhancement |
| Governance knowledge | RC13 | Framework coverage and repository mapping provenance | RC13 Governance Knowledge | `PASS` for current read-only truth model | First-class framework mapping enhancement planned |
| Real staging deployment identity | 8.1 | Environment, release/commit/images and owner evidence | Phase 8 Deployment Identity Record | `PENDING` | Approved immutable external deployment |
| Staging configuration parity | 8 | Infrastructure/runtime/configuration/IAM/TLS/data evidence | Phase 8 Staging Deployment-Parity Gate | `PENDING` | Same immutable staging identity |
| Staging functional validation | 8 | Deployed source-to-console and security/operations suites | Phase 8 gate | `PENDING` | Real staging environment |
| Independent penetration test | 9 | Independent report + disposition/retest | Phase 9 External Assurance Gate | `NOT COMPLETE` | External assessor and accepted target |
| Representative external load/stress | 9 | Production-equivalent performance report | Phase 9 gate | `NOT COMPLETE` | Production-equivalent target |
| Independent hardening/IAM/secrets review | 9 | External review evidence | Phase 9 gate | `NOT COMPLETE` | External assurance scope/target |
| Operational/stakeholder assurance | 9 | Independent/recorded approvals | Phase 9 / issue #1 | `NOT COMPLETE` | Human approvals and evidence |
| Production go/no-go | 10 | Complete evidence package and accountable decision | Roadmap + checklist | `NOT STARTED` | Accepted Phase 8 + Phase 9 |

## Product enhancement traceability

| Enhancement | Primary requirement | Planned evidence | Current state |
|---|---|---|---|
| E1 severity UX/filtering | Shared informational/low/medium/high semantics; accessible colours; consistent filtered metrics | Unit/contract/browser/WCAG + exact-head CI | `PLANNED / NEXT` |
| E2 manual source onboarding | Governed registration, validation, default-disabled, secret references, audit/RBAC | API/unit/browser/security tests | `PLANNED` |
| E3 trend analytics | 24h/7d/30d trends, volume vs severity distinction | Aggregation/unit/browser tests | `PLANNED` |
| E4 first-class framework mapping | Explicit versioned provenance-backed mappings | Data/API/governance contract tests | `PLANNED` |
| E5 deeper Administration RBAC | Role-permission matrix and governed assignment management | RBAC/security/browser/audit tests | `PLANNED` |
| E6 deeper Governance | Framework coverage, provenance/review and drill-down | Governance/API/browser evidence | `PLANNED` |

## Traceability rule

Every acceptance claim must be traceable from requirement to stage, QA/evidence family and the applicable execution or independent evidence.

Professional documents record the stable relationship and current decision. Exact workflow IDs, implementation chronology and point-in-time failures belong to the operational evidence layer (`docs/development/`, GitHub and CI artifacts).

A document or workflow definition without executed evidence is not sufficient for `PASS`.
