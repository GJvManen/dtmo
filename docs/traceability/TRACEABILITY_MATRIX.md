# DTMO Production Traceability Matrix

Last updated: 2026-08-10

| Requirement area | Roadmap phase | Primary evidence | Workflow / QA family | Current status | Remaining dependency |
|---|---:|---|---|---|---|
| CI integrity and regression protection | 1 | Exact-head GitHub Actions evidence | RC4 Quality Gate and workflow contracts | `PASS` | None internally |
| RBAC, identity, separation of duties | 2 | Security/identity tests and browser gates | RC4/RC9 security journeys | `PASS` internally | Production identity acceptance |
| Data integrity and recovery | 3 | Migration and recovery artifacts | RC6 recovery and object-storage migration | `PASS` internally | Full external restoration exercise |
| Connector reliability | 4 | Connector state/retry/timeout/replay/freshness evidence | RC7 connector gates | `PASS` internally | Production operational acceptance |
| Provenance and confidence | 4 | Payload provenance and connector evidence | RC7 Payload Provenance Gate | `PASS` internally | Ongoing source governance |
| Performance/scalability | 5 | Ingestion/read/queue/concurrency evidence | RC8 performance gates | `PASS` internally | Representative external load/stress |
| Automated accessibility | 6 | Browser/DOM accessibility artifacts | RC9 accessibility gates | `PASS` bounded | Genuine AT still required |
| VoiceOver/NVDA real behavior | 6 | Manual real-host evidence | External | `BLOCKED_EXTERNAL` | Real host/browser/screen-reader execution |
| Request observability | 7 | Request/trace artifacts | RC10 request/trace gates | `PASS` | None internally |
| Alerting and dashboards | 7 | Queue/storage/API/search/connector alerting evidence | RC10 alerting/dashboard gates | `PASS` | Operational delivery acceptance where applicable |
| Runbooks and exercises | 7 | Runbook and controlled exercise evidence | RC10 runbook gates | `PASS` | Organizational ownership maintained |
| Staging configuration contract | 8 | Emulator artifact | Phase 8 Staging Emulator Gate | `PASS` bounded | Does not prove real staging |
| Application-container runtime smoke | 8 | Runtime artifact | Phase 8 Staging Emulator Runtime Gate | `PASS` bounded | Does not prove complete dependency topology |
| Real staging deployment parity | 8 | Ten-class deployment package | Phase 8 Staging Deployment-Parity Gate | `BLOCKED_EXTERNAL` | Approved immutable staging deployment |
| Independent penetration test | 9 | Independent report + retest/disposition | Phase 9 External Assurance Gate | `NOT COMPLETE` | External assessor and target |
| Representative load/stress | 9 | External performance report | Phase 9 External Assurance Gate | `NOT COMPLETE` | Production-equivalent target |
| Full backup/restoration exercise | 9 | Exercise evidence | Phase 9 External Assurance Gate | `NOT COMPLETE` | Production-equivalent environment |
| Platform hardening | 9 | Hardened platform evidence | Phase 9 External Assurance Gate | `NOT COMPLETE` | Production platform |
| Secrets-management acceptance | 9 | Approved secret-manager/identity evidence | Phase 9 External Assurance Gate | `NOT COMPLETE` | Production secret path |
| Operational/stakeholder acceptance | 9 | Recorded approvals | Issue #1 / Phase 9 gate | `NOT COMPLETE` | Human approvals |
| Deployment acceptance | 9 | Staging + production acceptance record | Issue #1 / Phase 9 gate | `NOT COMPLETE` | Real deployment |
| Production go/no-go | 10 | Complete evidence set and approval | Roadmap + checklist | `NOT STARTED` | All prior blockers |

## Traceability rule

Every acceptance claim must be traceable from requirement to phase, QA gate, executable or independent evidence, PDCA run, pull request/merge where applicable, and authoritative issue state. A document or workflow definition without executed evidence is not sufficient for PASS.
