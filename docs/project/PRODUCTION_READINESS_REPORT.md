# DTMO Production Readiness Report

Assessment date: **2026-08-20**  
Software baseline: **16.0.0rc12 plus accepted post-RC13/E8/Phase-11 repository enhancements**

## 1. Executive conclusion

DTMO retains RC13 `PASS / OWNER_ACCEPTED`, E8.1–E8.10 `PASS / REPOSITORY_COMPLETE`, and historical Phase 8 `PASS / OWNER_ACCEPTED` plus Phase 9 `PASS / EXTERNAL_ASSURANCE_ACCEPTED` evidence for the earlier candidate. Phase 10 remains **`NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED`**. DTMO is **not production authorized**.

Phase 11 is `IN PROGRESS / ACTIVE`. Phase 11.1–11.9 and Phase 11.10a–11.10d are `PASS / REPOSITORY_COMPLETE`. Phase 11.10 remains **`IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED`**. The active bounded gate is **Phase 11.10e IntelOwl/Cortex integrated analysis**, `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED`. Phase 11.10f, Phase 11.10p, Phase 11.11 and Phase 12 are `NOT STARTED`.

## 2. Readiness summary

| Dimension | Current position | Decision |
|---|---|---|
| Engineering / CI | Accepted through Phase 11.9 plus 11.10a–11.10d workbench baseline | `PASS` within accepted scope |
| Functional product | Pre-workbench canonical journey owner accepted | `PASS / OWNER_ACCEPTED` historical baseline within scope |
| E8 scope | Repository complete | `PASS / REPOSITORY_COMPLETE` |
| Phase 8 | Historical prior-candidate validation | `PASS / OWNER_ACCEPTED` |
| Phase 9 | Historical prior-candidate assurance | `PASS / EXTERNAL_ASSURANCE_ACCEPTED` |
| Phase 10 | Production authorization | `NO-GO / BLOCKED` |
| Phase 11.1–11.9 | Integrations/runtime/migration | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10 | Candidate completion + production-equivalent validation | `IN PROGRESS / FRESH CANDIDATE-BOUND EVIDENCE REQUIRED` |
| Phase 11.10a | Frontend architecture/design | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10b | Canonical application shell | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10c | Command Center | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10d | Unified Intelligence Workspace | `PASS / REPOSITORY_COMPLETE` |
| Phase 11.10e | IntelOwl/Cortex integrated analysis | `IN PROGRESS / EXACT-HEAD VALIDATION REQUIRED` |
| Phase 11.10f | OpenCTI graph/entity workspace | `NOT STARTED` |
| Phase 11.10p | Fresh production-equivalent validation | `NOT STARTED / CANDIDATE FREEZE REQUIRED` |
| Phase 11.11 | Independent external assurance | `NOT STARTED` |
| Phase 12 | Formal production decision | `NOT STARTED` |

## 3. Accepted Phase 11 baseline

Taranis AI, IntelOwl, Cortex, OpenCTI, MISP and TheHive remain separate governed service/licensing boundaries. PostgreSQL remains canonical DTMO application truth. Provenance, **server-side RBAC**, least privilege, human publication/share authority, separate TheHive case authority and fail-closed evidence handling remain preserved.

Phase 11.8 accepted Kubernetes/Helm/GitOps runtime foundations, workload identity/external secret delivery, ingress/TLS/network segmentation, HA/disruption, observability, backup/recovery, supply-chain, capacity and exact prior-digest rollback controls. Phase 11.9 accepted the connected migration graph and forward-first compatibility model. Phase 11.10a/11.10b accepted the frontend architecture and canonical React/TypeScript/Vite `/workbench/` shell. Phase 11.10c accepted the canonical read-only Command Center. Phase 11.10d accepted the read-only Unified Intelligence Workspace. `/ui/console` remains a temporary **compatibility path**.

Normal browser operations follow **browser → DTMO API → governed integration adapter → upstream service**. The browser is not a privileged upstream client.

## 4. Active Phase 11.10e readiness boundary

The Analysis & Enrichment workspace is the next functional workbench slice in the materially changed candidate. It integrates governed IntelOwl enrichment and Cortex analyzer evidence in `/workbench/analysis`.

The implementation uses server-authorized DTMO contracts:

- `GET /api/v1/analysis/capabilities` for feature/allowlist visibility without inferred runtime health;
- `GET /api/v1/analysis/items/{item_id}/history` for persisted combined IntelOwl/Cortex evidence;
- `POST /api/v1/intelowl/items/{item_id}/enrich` for the existing explicit IntelOwl enrichment path;
- `POST /api/v1/analysis/items/{item_id}/cortex` for one explicit analyzer-only Cortex execution.

Reads remain protected by `read:intelligence`; execution requires server-side `review:intelligence`. Cortex responders, automatic analyzer discovery and automatic IntelOwl-to-Cortex fallback remain excluded. Durable Cortex records bind canonical item, stable job ID, observable, explicit analyzer, TLP and requesting principal. Persistence enforces `external_share_authorized=false` and `local_compromise_proven=false`.

Analyzer output is evidence rather than a verdict. It does not prove local compromise or grant publication/share, case or production authority. Capability configuration is not a live-health claim. Dependency, policy or persistence errors must **fail closed**, without synthetic successful analysis.

Repository/browser acceptance of 11.10e is engineering/functional evidence only. It **does not prove** live IntelOwl/Cortex availability or provider authorization, production-equivalent deployment, continuity, independent assurance or production authorization.

## 5. Candidate-completion sequence

After 11.10e, the fixed sequence remains 11.10f OpenCTI; 11.10g MISP; 11.10h TheHive; 11.10i Vulnerability/Exposure; 11.10j Sources/Collection; 11.10k Automation; 11.10l Governance/Evidence; 11.10m Operations/Admin; 11.10n role-aware UX/accessibility; and 11.10o consolidation/full functional acceptance.

One immutable integrated candidate is frozen only after 11.10o acceptance.

## 6. Phase 11.10p production-equivalent boundary

11.10p must bind one complete fresh evidence set to the **same immutable** candidate and one production-equivalent environment. Required classes remain:

- candidate identity/fingerprint;
- migration/compatibility;
- upgrade;
- exact prior-digest rollback plus post-rollback health;
- health/readiness;
- representative saturation/capacity;
- recovery/continuity and integrity/RPO/RTO observations where applicable.

Application rollback does not authorize automatic database down migration. Historical Phase 8/9 evidence is not reusable. Missing, inaccessible, placeholder, historical-only or mixed-candidate evidence must **fail closed**.

## 7. Explicitly unproven controls

A green repository workflow does not prove the new workbench has been deployed to the production-equivalent environment, that upstream services are healthy or complete, that real migration/rollback/recovery has occurred, or that production is authorized. Design mockups, generated visuals, browser mocks and repository fixtures are supporting engineering artifacts only.

## 8. Decision

Continue only **Phase 11.10e IntelOwl/Cortex integrated analysis** until its exact-head repository/browser/security/accessibility/integration regressions and professional documentation are fully green. Only after merge may Phase 11.10f start. Do not execute 11.10p or Phase 11.11 before candidate completion and immutable freeze.
