# DTMO Evidence Index

Last updated: **2026-08-17**

## Purpose

This index maps lifecycle stages to evidence classes and authoritative professional documentation. It is not a CI chronology. Exact run/commit/job history remains in immutable operational records, pull requests and CI artifacts.

**Current lifecycle:** Phase 8 is `PASS / OWNER_ACCEPTED`; Phase 9 is `PASS / EXTERNAL_ASSURANCE_ACCEPTED`; Phase 10 is `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`; Phase 11.1–11.5 are `PASS / REPOSITORY_COMPLETE`; Phase 11.6 TheHive handoff contract is `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`; Phase 12 is `NOT STARTED`. DTMO is not production authorized.

## Authoritative current-state sources

- `README.md`
- `docs/README.md`
- `docs/project/CURRENT_STATE.md`
- `docs/roadmap/PLATFORM_INDUSTRIALISATION_ROADMAP.md`
- `docs/architecture/THEHIVE_DTMO_HANDOFF_CONTRACT.md`
- `docs/integrations/THEHIVE_HANDOFF.md`
- `docs/operations/THEHIVE_HANDOFF_RUNBOOK.md`
- `docs/qa/PHASE11_6_THEHIVE_HANDOFF_CONTRACT_GATE.md`
- `backend/tests/test_thehive_handoff_contract.py`
- `.github/workflows/phase11-thehive-handoff-contract.yml`
- `docs/security/SECURITY_OVERVIEW.md`
- `docs/qa/QA_AND_RELEASE_GATES.md`
- `docs/roadmap/PRODUCTION_ROADMAP.md`
- `docs/project/PRODUCTION_READINESS_REPORT.md`
- `docs/project/PRODUCTION_CHECKLIST.md`
- `docs/project/EXECUTIVE_STATUS.md`
- `docs/project/DOCUMENTATION_STATUS.md`
- `docs/production/PHASE10_PRODUCTION_GO_NO_GO.md`

## Evidence hierarchy

1. **Repository-controlled engineering evidence** — exact-head CI, contracts, migrations and synthetic integration tests.
2. **Accountable functional evidence** — explicit owner acceptance of product behavior.
3. **Real-environment evidence** — production-equivalent validation bound to an immutable deployment identity.
4. **Independent assurance evidence** — external assessment independent from repository CI.
5. **Formal production authorization** — accountable GO/NO-GO for a specific candidate.
6. **Platform-integration evidence** — service contracts, adapters, mappings, migrations and interoperability evidence; never production authorization by itself.

## Lifecycle evidence map

### Phases 1–7

**Status:** `PASS`.

### RC13

**Status:** `PASS / OWNER_ACCEPTED`.

### E8.1–E8.10

**Status:** `PASS / REPOSITORY_COMPLETE`.

### Phase 8

**Status:** `PASS / OWNER_ACCEPTED` for the earlier candidate.

### Phase 9

**Status:** `PASS / EXTERNAL_ASSURANCE_ACCEPTED` for the earlier candidate.

### Phase 10

**Status:** `NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`.

### Phase 11.1–11.5

**Status:** `PASS / REPOSITORY_COMPLETE`.

Accepted repository evidence covers Taranis, IntelOwl, OpenCTI and MISP service boundaries, identity/provenance preservation, durable reconciliation/state, fail-closed authority controls and human publication/share authority. These are repository engineering claims only.

### Phase 11.6 TheHive handoff contract

**Status:** `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`.

The active repository evidence target covers:

- TheHive 5.5.16 and public API v1 (`/api/v1`) as reviewed upstream baseline;
- TheHive remaining a separate StrangeBee service with no source vendoring or inferred license entitlement;
- explicit recognition that TheHive 5.3+ requires an activated Community/Gold/Platinum license for continued write operation;
- `POST /api/v1/case` being only a mutation candidate after explicit human-authorized DTMO case handoff;
- case-handoff authority remaining separate from publication/share authority;
- stable DTMO canonical identity, handoff request/idempotency identity, TheHive case identity and organization context being required for durable reconciliation;
- blind replay being prohibited after ambiguous mutation delivery;
- TLP/PAP/access restrictions never being broadened and unknown/unrepresentable restrictions failing closed;
- least-privilege non-human TheHive identity and runtime-secret handling;
- attachments, raw source bodies, credentials, private enrichment and unrelated personal data being excluded by default;
- TheHive case lifecycle not becoming canonical CTI truth, local-compromise proof or DTMO external-share authority;
- responders, Cortex execution, automatic MISP→TheHive automation, external sharing and administration remaining excluded;
- professional architecture, integration, operations, security, QA, roadmap, evidence and current-state documentation remaining synchronized.

The dedicated contract test/workflow are `backend/tests/test_thehive_handoff_contract.py` and `.github/workflows/phase11-thehive-handoff-contract.yml`.

Repository contract acceptance does **not** prove live TheHive connectivity, deployed service-account permissions, activated license entitlement, organization/access configuration, privacy approval, correct TLP/PAP handling on real data, HA/recovery, production-equivalent validation, independent assurance or production authorization.

### Phase 11.7–11.9

Future evidence covers the conditional Cortex disposition, Kubernetes/Helm/GitOps runtime hardening and migration/compatibility in fixed order.

### Phase 11.10–11.11

Fresh production-equivalent validation and fresh independent assurance must target the same immutable integrated candidate. Historical Phase 8/9 evidence cannot satisfy these gates.

### Phase 12

**Status:** `NOT STARTED`.

## Evidence transfer rule

Historical Phase 8/9 acceptance remains candidate-bound and cannot be transferred automatically to the materially changed Phase 11 platform.

## Governance and handling rules

Framework claims remain governed by explicit provenance-backed mappings. External service state does not establish local exploitability, compromise, case necessity or dissemination authority without separate attributable evidence.

- Exact-head evidence belongs only to the exact state tested.
- Missing, queued, skipped, cancelled, failed, stale or inaccessible evidence is not `PASS`.
- Credentials/tokens and unnecessary personal data do not belong in repository evidence.
- Human review/share approval and human case-handoff approval remain separate from technical execution.
- Historical immutable run records are never rewritten to manufacture later acceptance.
