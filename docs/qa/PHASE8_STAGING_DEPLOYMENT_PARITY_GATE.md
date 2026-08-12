# Phase 8 — Production-Equivalent Staging Deployment-Parity Gate

**Status:** `READY_FOR_EXTERNAL_VALIDATION / PENDING_EXTERNAL_DEPLOYMENT_IDENTITY`

## Objective

Phase 8 establishes that the accepted DTMO product can be deployed and operated in one approved production-equivalent staging environment with evidence tied to a single immutable deployment identity.

This gate deliberately separates real deployed-environment evidence from repository CI, local Docker Compose and synthetic staging/browser fixtures.

## Entry condition

The Phase 8 entry condition is satisfied:

- Phases 1–7: `PASS`;
- RC13 functional console: `PASS / OWNER_ACCEPTED`;
- accountable owner acceptance recorded;
- no production-readiness claim has yet been made.

Issue #158 is the active Phase 8.1 work item.

## Phase 8.1 — immutable deployment identity

Before staging validation can be credited, one immutable deployment identity must be established.

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

Required evidence includes:

- platform/runtime versions;
- PostgreSQL, OpenSearch, Redis and object-storage configuration;
- persistence volumes/storage classes;
- backup/recovery configuration relevant to the staging acceptance scope;
- application environment/configuration parity;
- approved deviations with rationale/risk disposition;
- observability/metrics/logging configuration;
- separately authenticated Grafana operations access.

## Network and TLS evidence

- approved ingress path;
- TLS certificate and termination details;
- administrative/operational access restrictions;
- required source egress connectivity;
- network segmentation/restriction evidence as applicable;
- no anonymous operational dashboard access.

## Data and privacy evidence

- staging data classification;
- approved synthetic/sanitized/representative data approach;
- confirmation that production credentials are absent;
- confirmation that unnecessary personal data is not used;
- retention/deletion expectations;
- evidence-export minimization for logs, screenshots and artifacts.

## Deployment-time security review

The immutable deployment identity must be accompanied by a review of:

- application dependencies;
- container/base images;
- relevant CVEs/vendor advisories;
- deployment configuration/hardening;
- outstanding findings and accountable disposition.

## Deployed acceptance suites

All suites below must run against the same deployment identity.

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

### Source and intelligence pipeline

- source catalog/bootstrap;
- source activation;
- supported source fetch;
- raw evidence persistence;
- normalization;
- canonical PostgreSQL commit;
- OpenSearch indexing;
- Intelligence visibility;
- dashboard/analytics aggregation.

### Canonical product

- Overview;
- Intelligence;
- Sources & Catalog;
- Visual Analytics;
- Administration;
- Governance;
- supported browser/interaction expectations.

### Operations and resilience

- alert/metrics visibility;
- logging/correlation;
- operational runbook applicability;
- agreed backup/restore/recovery validation;
- rollback readiness.

## Acceptance rule

Phase 8 may be marked `PASS` only when:

1. the immutable staging identity is complete and approved;
2. required configuration/security/privacy evidence is reviewable;
3. deployed suites succeed against that exact identity;
4. contradictory, stale or missing evidence is resolved;
5. accountable staging/project acceptance is explicitly recorded.

Repository CI, local Docker Compose, staging emulators and synthetic browser fixtures cannot satisfy this gate by themselves.

## Governance boundaries

Phase 8 does not alter publication authority. Staging access, source execution, Administration, Governance, CI or operational dashboard access cannot approve external sharing.

## Current priority

**Provision and evidence the real approved Phase 8.1 staging environment and immutable deployment identity.**
