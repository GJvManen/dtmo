# Phase 8 — Production-Equivalent Staging Deployment-Parity Gate

**Status:** `ACTIVE_EXTERNAL_VALIDATION / OWNER_APPROVED_STAGING / IMMUTABLE_EVIDENCE_BINDING_INCOMPLETE`

## Objective

Phase 8 establishes that the accepted DTMO product can be deployed and operated in one approved production-equivalent staging environment with evidence tied to a single immutable deployment identity.

This gate deliberately separates real deployed-environment evidence from repository CI, local Docker Compose and synthetic staging/browser fixtures.

## Entry condition

The Phase 8 entry condition is satisfied:

- Phases 1–7: `PASS`;
- RC13 functional console: `PASS / OWNER_ACCEPTED`;
- E8.1–E8.10: `PASS / REPOSITORY_COMPLETE`;
- post-E8 external deployment: `PASS / OWNER_VERIFIED_EXTERNAL_EVIDENCE`;
- production-equivalent staging environment: `APPROVED / OWNER_VERIFIED_EXTERNAL_EVIDENCE`;
- no production-readiness claim has yet been made.

Issue #158 remains the active Phase 8 evidence-binding work item.

## Phase 8.1 — deployment and immutable identity binding

On 2026-08-15 the accountable owner confirmed that the post-E8 deployment had been extensively and successfully tested externally and that the production-equivalent staging environment is approved. The prior blocker requiring a real external deployment and approved staging environment is therefore closed.

Formal Phase 8 closure still requires that the accepted deployment be bound to one immutable technical identity. This is evidence completion and does not by itself require a redeployment.

### Required identity fields

1. approved staging environment identifier;
2. accountable staging owner;
3. approved reachable endpoint/access path;
4. deployed DTMO release;
5. exact Git commit;
6. immutable application image digest;
7. immutable supporting service image digests;
8. infrastructure/runtime inventory;
9. configuration baseline/parity reference;
10. deployment/change record;
11. rollback target/procedure;
12. deployment-time security-review record.

No Phase 8 functional evidence may be combined across different deployments or inferred from a later/earlier image.

## Identity and secrets requirements

The staging identity model must preserve least privilege:

- application/service identities are separate from infrastructure root/admin identities;
- human/admin roles remain separate from service-account roles;
- secrets are resolved through approved staging secret-management mechanisms;
- repository evidence contains secret references, never raw secret values;
- local-development AIStor root/bootstrap credential compatibility is **not** used as the staging identity model;
- production credentials are not reused in staging;
- bearer-token issuer/audience/key trust is explicitly documented for staging.

## Infrastructure and configuration parity

Required evidence includes platform/runtime versions; PostgreSQL, OpenSearch, Redis and object-storage configuration; persistence/storage configuration; backup/recovery configuration relevant to the staging scope; application configuration parity and approved deviations; observability/metrics/logging configuration; and separately authenticated Grafana operations access.

## Network, TLS, data and privacy evidence

Evidence must cover the approved ingress path, TLS termination, administrative/operational access restrictions, required source egress connectivity, applicable network restrictions, staging data classification, synthetic/sanitized data handling, absence of production credentials, retention/deletion expectations and evidence-export minimization.

## Deployment-time security review

The immutable deployment identity must be accompanied by a review of application dependencies, container/base images, relevant CVEs/vendor advisories, deployment hardening and outstanding findings with accountable disposition.

## Phase 8.2 — deployed platform and identity validation

**Status:** `IN PROGRESS / ACTIVE`

All Phase 8.2 suites must run against the accepted post-E8 staging deployment and be bound to the same immutable identity before formal acceptance.

### Platform health

- health/readiness;
- PostgreSQL connectivity and migrations;
- OpenSearch health/search;
- Redis coordination;
- object-storage read/write contract;
- Prometheus/operational metrics;
- separately authenticated Grafana operational access.

### Identity and authorization

- bearer-token trust validation;
- role/permission enforcement;
- service-account/human separation;
- privileged Administration protections;
- audit/correlation behavior;
- separate review/external-share authority.

## Phase 8.3 — source and intelligence validation

The same identity must cover source catalog/bootstrap, source activation, supported source fetch, raw evidence persistence, normalization, canonical PostgreSQL commit, OpenSearch indexing, Intelligence visibility and dashboard/analytics aggregation, including the accepted E8 vulnerability/CTI surfaces.

## Phase 8.4 — operations and resilience

The same identity must cover alert/metrics visibility, logging/correlation, operational runbook applicability, agreed backup/restore/recovery validation and rollback readiness.

## Phase 8.5 — accountable acceptance

Phase 8 is complete only when the immutable staging identity is complete and approved; required configuration/security/privacy evidence is reviewable; deployed suites succeed against that identity; contradictory, stale or missing evidence is resolved; and accountable staging/project acceptance is explicitly recorded.

Repository CI, local Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this gate by themselves.

## Governance boundaries

Phase 8 does not alter publication authority. Staging access, source execution, Administration, Governance, CI or operational dashboard access cannot approve external sharing.

## Current priority

**Execute Phase 8.2 platform and identity validation against the owner-approved post-E8 staging deployment while completing immutable evidence binding for that same deployment.**
