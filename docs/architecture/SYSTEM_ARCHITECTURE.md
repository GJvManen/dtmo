# DTMO System Architecture

Last updated: **2026-08-11**  
Current baseline: **16.0.0rc12**

## Purpose

DTMO is an education-focused Cyber Threat Intelligence platform that collects official threat/vulnerability intelligence, normalizes it with provenance, supports governed investigation and administration, and presents operational and intelligence analytics without collapsing human approval boundaries.

## Logical architecture

```mermaid
flowchart LR
    EXT[Official external intelligence sources] --> CF[Source adapter / connector framework]
    CF --> NP[Normalization & provenance]
    NP --> API[FastAPI application services]

    API --> PG[(PostgreSQL)]
    API --> OS[(OpenSearch)]
    API --> RD[(Redis)]
    API --> OBJ[(Object evidence storage)]

    API --> PM[Prometheus]
    PM --> GF[Grafana]
    PG -->|explicit reporting views| GF

    USER[Analyst / Admin / CISO / Auditor] --> GW[Nginx gateway]
    GW --> CONSOLE[Unified DTMO console]
    CONSOLE --> API
    GW -->|/grafana/| GF

    API --> GOV[RBAC / audit / review / share-approval controls]
```

## Architecture layers

### 1. Source ingress

Provider-specific adapters operate through the governed source framework. Execution is bounded by explicit source identity, supported execution profiles, timeout/retry behavior, fail-closed parsing and provenance retention.

Credentialed sources use logical secret references; credential values are resolved at runtime and are not stored in the source catalog.

### 2. Normalization and provenance

Provider payloads are converted into canonical intelligence records while preserving source identity, raw evidence references, confidence and relevant publication metadata. Missing enrichment is not invented.

### 3. Application and API

The Python 3.12+/FastAPI application provides authenticated APIs, source operations, search/investigation, administration, metrics and governance workflows.

The canonical browser product is the **unified DTMO console**. Legacy role/workspace routes may remain for compatibility but are not separate intended product shells.

### 4. Persistence and search

| Component | Responsibility |
|---|---|
| PostgreSQL 17 | relational application state, governance state and explicit Grafana reporting views |
| OpenSearch 2.19 | intelligence search/index state |
| Redis 8 | cache/queue and runtime coordination state |
| S3-compatible AIStor/MinIO interface | object/evidence storage |

### 5. Observability and analytics

Prometheus collects bounded application/operational metrics. Grafana provides DTMO Operations and DTMO Intelligence dashboards.

Grafana intelligence access uses a **dedicated least-privilege database reader** restricted to explicit reporting views. It does not reuse the DTMO application database identity. Anonymous Grafana access is disabled.

The Nginx gateway exposes Grafana to the browser through the managed same-origin `/grafana/` path. Native DTMO chart/table alternatives remain available for accessible fallback and bounded summary use.

### 6. Gateway and browser boundary

The Nginx gateway is the managed browser-facing boundary for the canonical application and embedded Grafana path. Application/API authorization remains server-side; the gateway and presentation layer do not grant application authority.

### 7. Governance and approval

Security-sensitive authorities are deliberately separated:

- source administration and execution;
- intelligence analysis;
- human review;
- external share approval;
- audit/read-only access;
- CISO/security administration.

Technical execution, CI success, connector access, dashboard access or staging access cannot authorize publication or external sharing.

## Principal technology stack

- Python 3.12+
- FastAPI / Uvicorn
- SQLAlchemy / Alembic
- PostgreSQL 17
- Redis 8
- OpenSearch 2.19
- S3-compatible object evidence storage
- Prometheus 3
- Grafana 13
- Nginx
- Docker Compose reference topology

## Trust boundaries

Important trust boundaries are:

1. external provider networks → connector/source ingress;
2. unauthenticated client → authenticated application boundary;
3. authenticated role → privileged administrative/review/share actions;
4. application → database/search/cache/object services;
5. Grafana → explicit reporting boundary;
6. browser → Nginx/application/Grafana same-origin gateway;
7. repository CI/emulator → real staging/production environment;
8. technical execution → human publication/share authority.

## Reliability and resilience

Connector behavior has explicit state, retry, timeout, replay, freshness and failure-isolation controls. Repository-controlled recovery gates cover multi-store migration/recovery behavior and integrity checks.

This engineering evidence does not replace the external requirement for a production-equivalent backup/restoration exercise or a real staging acceptance decision.

## CI and release architecture

The release process is exact-head gated. Pull requests pass registered quality, security, connector, recovery, performance, browser/accessibility, observability and staging-readiness workflows before expected-head protected merge.

Repository evidence is intentionally separated from external acceptance. CI, Docker Compose and staging-emulator success demonstrate engineering behavior; they do not establish real staging or production readiness.

## Current acceptance boundary

Phases 1–7 are accepted. Phase 6's final external/manual blocker was closed by accountable project-owner acceptance on 2026-08-11.

Phase 8 is `READY_FOR_EXTERNAL_VALIDATION`: the project owner will validate one immutable production-equivalent `16.0.0rc12` staging deployment against the ten-class deployment-parity gate after the final repository cleanup is accepted.

## Security invariants

- RBAC and least privilege;
- separation of duties;
- human share approval separate from review and technical access;
- provenance and confidence preservation;
- privacy and data minimization;
- auditable state transitions and request correlation;
- no secret values in repository evidence;
- no automatic publication from CI, connectors, recovery, analytics or runtime success.
