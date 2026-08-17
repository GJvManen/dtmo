# Phase 11.6 TheHive Handoff Implementation Gate

Status: **`ACTIVE / EXACT-HEAD VALIDATION REQUIRED`**

## Purpose

This gate accepts only the bounded repository implementation of explicit human-authorized DTMO→TheHive case handoff and durable mutation reservation/reconciliation state. It does not establish live TheHive entitlement, credentials, connectivity, privacy approval, operational readiness or production authorization.

## In-scope acceptance

The exact PR head must prove:

- `handoff:case` exists as a dedicated server-side RBAC permission distinct from `approve:share`;
- routine service accounts cannot authorize handoff;
- the external mutation surface is limited to `POST /api/v1/case`;
- canonical item identity and repository provenance are required;
- severity, TLP and PAP mappings are explicit and unknown values fail closed;
- a requested TLP cannot broaden a known authoritative TLP tag;
- authoritative MISP distribution/sharing-group restrictions block handoff until a deployment-approved TheHive access mapping exists;
- the minimized payload excludes attachments, raw source bodies, credentials and private enrichment output;
- `thehive_handoff_state` is durably committed before external mutation;
- request UUID and confirmed TheHive case identity are unique;
- confirmed stable case identity becomes `delivered`;
- timeout/network uncertainty or success without stable identity becomes `ambiguous`;
- `delivered` and `ambiguous` requests cannot be blindly replayed;
- persisted upstream outcome is minimized to case identity/number/organization rather than arbitrary response content;
- database constraints enforce `external_share_authorized=false` and `local_compromise_proven=false`;
- production configuration requires HTTPS API base, runtime token and explicit organization when the feature is enabled;
- all affected authoritative architecture, integration, security, operations, user/admin, QA, evidence and roadmap documentation is synchronized.

## Required checks

The dedicated workflow runs the Phase 11.6 adapter/state tests, TheHive contract regression tests and professional documentation contract. RC4 Quality Gate and Professional Documentation Gate remain mandatory repository-wide acceptance checks.

## Fail-closed rule

Any failed, skipped, cancelled, stale, missing or inaccessible required check is not acceptance. A new commit invalidates earlier exact-head evidence.

## Explicit non-evidence

A green gate does **not** prove:

- live TheHive connectivity or tenant health;
- activated Community/Gold/Platinum entitlement or quota;
- effective service-account permissions or organization membership;
- privacy/legal approval for real case data;
- real-data TLP/PAP/access correctness;
- HA, recovery, capacity or upgrade readiness;
- Phase 11.10 production-equivalent validation;
- Phase 11.11 independent assurance;
- Phase 12 production authorization.

Historical Phase 8/9 evidence remains bound to the earlier candidate and cannot satisfy these later gates.

## Exclusions

This gate does not accept automatic case creation, task/observable mutations, responders, Cortex execution, automatic MISP→TheHive workflows, external sharing, case deletion, organization/platform administration or production use.
