# DTMO Frontend Release Gate

**Status:** `PASS` for the accepted `16.0.0rc12 / RC13` frontend baseline

## Objective

Define the repository-controlled release contract for the canonical DTMO web application while preserving server-side authorization, security headers, accessibility and separate human approval boundaries.

This gate is a durable frontend contract. Exact workflow/run history belongs to the operational evidence layer.

## Canonical product surface

The accepted frontend must expose the unified console at the documented application entry point and provide coherent navigation across:

1. Overview;
2. Intelligence;
3. Sources & Catalog;
4. Visual Analytics;
5. Administration;
6. Governance.

Specialized or supporting role views may remain where useful, but they must not fragment the normal canonical product journey.

## Required security behavior

- Server-side RBAC remains authoritative; hidden/disabled controls are UX only.
- Human and service-account authority remains separated.
- Review and external-share approval remain separate permissions/actions.
- Privileged Administration actions retain server authorization and auditability.
- Credentials/tokens are not embedded in HTML or source-controlled frontend assets.
- Production authentication remains the configured bearer-token/identity-provider model.
- CSP, anti-framing, no-sniff and appropriate no-store/referrer protections remain in force for dynamic application responses.
- No frontend convenience introduces anonymous Grafana access or an authorization bypass.

## Required functional behavior

- Canonical navigation works under supported browser evidence.
- Overview refresh exposes truthful loading/success/partial-failure/empty states.
- Intelligence renders durable canonical application records.
- Sources & Catalog actions invoke governed source operations.
- Visual Analytics renders meaningful populated or explicit empty states.
- Administration exposes governed user/role assignment state without mixing source management into the primary administration workflow.
- Governance renders truthful framework/mapping evidence states.
- Browser page and console errors remain within accepted zero-error functional journeys where specified by the relevant gate.

## Accessibility and UX behavior

The frontend must preserve:

- semantic headings and controls;
- keyboard-operable actions;
- visible focus;
- skip-navigation/supporting landmarks where applicable;
- responsive reflow;
- text resize/spacing resilience;
- measurable contrast;
- reduced-motion handling where relevant;
- live/semantic status messaging;
- non-colour cues for state/severity.

Any future severity colour enhancement must not encode risk by colour alone.

## Evidence

Frontend changes require focused unit/contract/browser evidence plus the complete required exact-head workflow matrix for the final PR head.

A new commit invalidates earlier exact-head CI. Workflow presence, queued execution, partial success or stale-head evidence is not `PASS`.

## Claim boundary

A PASS for this gate establishes the repository-controlled frontend contract and accepted functional baseline. It does not itself establish real Phase 8 staging, Phase 9 independent assurance or Phase 10 production approval.

## Enhancement boundary

The next frontend enhancement is a shared accessible severity/filter contract for Overview and Intelligence. It must preserve all requirements above and pass fresh exact-head release evidence before merge.
