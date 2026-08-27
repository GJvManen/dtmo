# Threat Intelligence default datapath recovery

## Objective

Complete the next bounded functional-recovery step after Sources & Collection by connecting the canonical Threat Intelligence population control to the supported built-in source path that is available from a clean supported installation.

## Verified integration defect

The Sources & Collection recovery made the built-in CISA KEV source visible and runnable through the Source Center runtime model. Threat Intelligence still only inspected registered `/api/v1/admin/sources` entries, so a clean installation could expose `Load CISA KEV now` in Sources & Collection while the empty Threat Intelligence workspace continued to report that no governed source was enabled.

That split meant the operator still lacked a coherent clean-install sequence from source readiness to useful intelligence content.

## Recovery

`ThreatIntelligencePopulation` now reads both the registered source registry and `/api/v1/source-center/status`. It keeps existing enabled registry-source execution unchanged and additionally exposes supported built-in sources only when `manual_run_available` is true. Built-in execution uses the existing server-side `/connectors/{source_id}/run` contract; it does not duplicate connector logic in the browser.

After successful collection, the operator can explicitly reload recent canonical intelligence. The same persisted canonical dataset is then available to the existing Threat Intelligence discovery/detail workflow and IOC Explorer projections where applicable.

## Security and authority boundaries

The browser still requires a session with `manage:connectors` before source execution controls are presented. Registered sources must already be enabled. Built-in sources are shown only when server-side Source Center readiness permits a manual run. The browser does not enable `feature_live_connectors`, change endpoints, inject credentials or bypass production deployment switches.

Successful CISA KEV collection proves only attributable canonical ingestion. It does not prove exploitation, local compromise, remediation status, review approval, publication authority or external sharing authority.

## Acceptance boundary

Repository checks prove the canonical wiring and security contract. They are not owner functional acceptance, not staging evidence and not production-equivalent evidence. The next owner test must execute the clean supported installation flow end to end: open Threat Intelligence with no content, load CISA KEV through the exposed governed built-in path, reload canonical intelligence, verify useful discovery/detail, and confirm the resulting data is available through the IOC Explorer where the canonical projection applies.
