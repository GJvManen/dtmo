# DTMO Continuous Development Operating Model

## Purpose

DTMO is managed as a continuous development project. Work is performed in bounded, auditable runs. Each run must improve the repository, validate a hypothesis, reduce a blocker, or explicitly record why no safe change could be made.

## Virtual worker structure

The development program uses the following coordinated workstreams:

| Worker stream | Responsibility | Primary evidence |
|---|---|---|
| Product & Architecture | Roadmap, ADRs, service boundaries, release scope | ADRs, roadmap, release notes |
| Backend Platform | FastAPI, persistence, scheduling and service integration | Code, API tests, migrations |
| Connector Engineering | Live feeds, retries, rate limits and source contracts | Contract tests, health reports |
| Intelligence Engineering | Normalisation, deduplication, provenance and quality | Receipts, lineage, quality reports |
| Knowledge Graph | Entity resolution, relationships and confidence | Graph tests, evidence links |
| Search & Analytics | OpenSearch, filters, trends and performance | Search tests, benchmarks |
| Frontend & UX | SOC/CISO/Privacy workspaces and accessibility | E2E, WCAG and visual evidence |
| Security & Privacy | RBAC, secrets, logging, data minimisation and threat modelling | Security tests, threat model |
| QA & Release | Regression, CI, coverage, release gates and defect triage | Workflow results, QA reports |
| Documentation | Architecture, operations, user and run documentation | Maintained Markdown documentation |

These are coordinated workstreams, not autonomous external identities. Every output remains subject to the same repository controls and human publication approval.

## Run lifecycle

1. **Inspect** the repository, open issues, latest commits and current CI evidence.
2. **Select** exactly one highest-value bounded objective.
3. **Implement** code, tests, documentation or issue updates.
4. **Validate** using available automated checks and static review.
5. **Document** the run in `docs/development/RUN_LOG.md` and issue #2.
6. **Gate** the run as `PASS`, `BLOCKED` or `NO-CHANGE`.
7. **Queue** the next concrete action.

## Run quality rules

- Never report a test as passed unless the result is available.
- A missing GitHub Actions status is `PENDING`, not `PASS`.
- Every production-impacting change requires tests and documentation.
- Every connector must preserve source URL, retrieval time, content hash and reliability.
- Intelligence starts as `candidate` and may not be shared without separate approval.
- Reports without evidence are rejected.
- Secrets are never committed.
- Destructive migrations require an explicit rollback procedure.

## Prioritisation

Work is prioritised in this order:

1. broken builds or security blockers;
2. data integrity and provenance defects;
3. authentication, authorisation and auditability;
4. production adapters and service integration;
5. connector reliability and source expansion;
6. frontend usability and accessibility;
7. performance and scale;
8. additional features.

## Definition of done for a run

A run is complete only when it has:

- a unique run ID;
- an explicit objective;
- a commit, issue update, or documented blocker;
- test or review evidence;
- known limitations;
- a next action;
- a releasegate status.

## Release gates

### PASS

The bounded objective is implemented and supported by available evidence. This does not imply that the complete product is production-ready.

### BLOCKED

A required dependency, credential, environment, approval or failing test prevents completion. The blocker must be concrete and actionable.

### NO-CHANGE

Inspection found no safe, justified change for that run. The reason and next trigger must be documented.

## Continuous-development control issue

GitHub issue #2 is the program control record. Material runs should add a short summary there, while the full chronological record remains in `RUN_LOG.md`.
