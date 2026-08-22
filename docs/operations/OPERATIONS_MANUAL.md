# DTMO Operations Manual

Last updated: **2026-08-21**  
Baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## Purpose

This manual describes the durable operational control model for DTMO. Component-specific procedures remain in their runbooks. Operational incident chronology belongs in attributable tickets/run evidence rather than this manual.

## Daily operational checks

Operators should verify application health/readiness; PostgreSQL, OpenSearch, Redis and object-storage health; connector/source state and freshness; queue/backlog condition; recent alert state; search/storage integrity; scheduled activity; dashboards; and unresolved incident/change items.

Operational review preserves privacy: raw sensitive payloads, tokens and credentials do not belong in tickets, chat or repository evidence unless explicitly required and approved.

## Access and authority

Operational access is role-based and least privilege. Technical access does not grant intelligence review, case handoff, external-share approval, publication or production authority. Service identities do not acquire human administrator/reviewer/publisher powers.

`read:intelligence`, `review:intelligence`, `approve:share`, `handoff:case`, `manage:connectors` and administrative permissions remain distinct server-side authorization domains.

## Connector, source and automation operations

Connector/source failures use the accepted state, retry/backoff, timeout, replay, freshness, failure-isolation, normalization/provenance and canonical-persistence controls. Troubleshooting preserves source/provider provenance, timestamps, correlation identifiers and confidence/context. Raw/search writes are not by themselves proof of canonical PostgreSQL-backed application state.

Source and upstream credential values remain server-side. Validation, collection or automation success does not prove source truth, compromise, remediation, review completion, publication/share authority, production-equivalent operation or production authorization.

## Governance & Evidence operations — Phase 11.10l

The canonical `/workbench/governance` workspace is read-oriented and uses DTMO-owned `GET /api/v1/governance/knowledge`. Operational users may use it to inspect repository-backed governance state, but mapping visibility does not create an operational mutation or approval path.

The active governance snapshot reuses the explicit typed crosswalk in `backend/dtmo/governance_crosswalk.py` and `docs/governance/GOVERNANCE_MAPPING_REGISTRY.md`. Normenkader IBP, MITRE ATT&CK and NIST CSF relationships are partial and scoped; CVSS is context-only. Unrecorded objects remain unmapped. Missing/inaccessible governance evidence **fails closed** and must not be translated into PASS, compliant or healthy state.

A displayed mapping does not prove certification, complete compliance, environment effectiveness, local compromise, audit acceptance or remediation. Governance visibility grants no review, case, connector, share, publication, administration or production authority.

## Monitoring and alerting

Repository-controlled gates verify alerting/observability contracts, request correlation, storage/search health controls, queue/backlog controls and relevant dashboard configuration. Configuration does not equal live runtime health. Operators must distinguish configured capability from attributable runtime observation.

## Backup, restore, recovery and rollback

Accepted Phase 11 recovery controls require provenance-bound backup/restore evidence and exact prior immutable application identity for rollback. Application rollback does not authorize automatic database down migration. Real recovery effectiveness for the final integrated candidate remains a Phase 11.10p production-equivalent evidence requirement.

## Current lifecycle and evidence boundary

Phase 8 remains `PASS / OWNER_ACCEPTED — HISTORICAL CANDIDATE`; Phase 9 remains `PASS / EXTERNAL_ASSURANCE_ACCEPTED — HISTORICAL CANDIDATE`; Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**.

Phase 11.1–11.9 and Phase 11.10a–11.10k are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`** with Phase 11.10l `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10m–11.10o, Phase 11.11 and Phase 12 are `NOT STARTED`; Phase 11.10p is `NOT STARTED / CANDIDATE FREEZE REQUIRED`. DTMO is **not production authorized**.

Repository CI is repository engineering evidence only. Historical Phase 8/9 evidence cannot be reused for the materially changed candidate. Production-equivalent validation must be fresh for one immutable candidate after 11.10a–11.10o completion, followed by independent Phase 11.11 assurance and the later Phase 12 formal GO/NO-GO.
