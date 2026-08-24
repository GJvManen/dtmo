# Phase 11.10q — Threat Intelligence canonical population recovery

## Scope

This recovery slice connects the existing governed `ThreatIntelligencePopulation` control to the canonical Threat Intelligence empty state. It is intentionally bounded to population of canonical DTMO persistence from an already-enabled governed source and refresh of the recent/default discovery view.

## Operator flow

When `/workbench/intelligence` has no canonical recent intelligence, the workspace now shows an actionable population control instead of only an empty-state explanation. The control reads the authenticated same-origin session, lists registered sources through `/api/v1/admin/sources`, and exposes execution only for sources already marked enabled. A source run uses the existing audited `/api/v1/admin/sources/{source_id}/run` contract with a request ID. After a completed run the operator explicitly chooses **Reload recent intelligence**, which re-reads `/api/v1/command-center` and repopulates the canonical recent view from persistence.

## Authority and evidence boundaries

This workspace does not activate sources, change connector endpoints, receive or edit credentials, approve intelligence, publish content, authorize external sharing or infer source health from a failed run. Source activation/configuration remains in Sources & Collection under the existing server-side authorization boundary. A successful run reports connector execution/ingestion evidence only; review and sharing remain separate governed decisions.

The default intelligence list remains canonical persistence-backed. No synthetic intelligence is generated when persistence is empty, and repository-controlled execution or acceptance evidence must not be represented as live-source, staging, production-equivalent or external-assurance evidence.

## Acceptance impact

This removes the empty-state-only defect for Threat Intelligence by giving an authorized operator a same-origin path to populate and reload canonical intelligence without opening a legacy `/ui/*` route. It does **not** by itself clear the owner functional rejection. `docs/roadmap/FUNCTIONAL_RECOVERY_ACCEPTANCE.md` remains authoritative and Threat Intelligence stays blocked until the owner retest confirms the normal deployment path is usable with real configured sources and attributable content.
