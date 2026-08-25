# Cortex analyzer policy recovery

## Purpose

Cortex already has a governed analyzer execution path in the canonical Analysis & Enrichment workspace. The remaining Administration gap is configuration: shared integration readiness requires a non-empty `cortex_allowed_analyzers` policy, but the canonical Administration control plane does not yet expose or persist that policy.

This recovery slice makes the Cortex analyzer allowlist a first-class non-secret Administration setting without moving analyzer execution into Administration.

## Required canonical behavior

An authorized principal with `manage:connectors` must be able to configure the Cortex API endpoint, write-only credential, enablement and **Cortex analyzer allowlist** through the same-origin Administration API and workspace.

The allowlist is non-secret runtime policy and belongs in the existing runtime integration settings document. Credentials remain separately server-side and are never returned to the browser.

Canonical Administration must consume the shared `integration_readiness()` result for Cortex. Endpoint plus credential alone must therefore remain `configuration-required` while the analyzer allowlist is empty, with **Cortex analyzer allowlist** reported as an activation blocker.

## Execution boundary

Administration configures Cortex but does not execute analyzers. **Run Cortex** remains in the governed Analysis & Enrichment workflow, where the existing authorization, canonical-object context, persisted result history and evidence-not-verdict boundaries remain authoritative.

A configured allowlist is not runtime-health evidence and does not prove analyzer availability, successful execution, local compromise or remediation. Configuration grants no review, sharing, publication, responder, external-assurance or production authority.

## Fail-closed requirements

Cortex analyzer policy submitted for a non-Cortex integration must be rejected. Unsaved browser policy must not be treated as persisted readiness. Missing endpoint, credential or analyzer allowlist must continue to block activation according to shared server-derived readiness.

OpenCTI and TheHive configuration are intentionally outside this bounded slice.
