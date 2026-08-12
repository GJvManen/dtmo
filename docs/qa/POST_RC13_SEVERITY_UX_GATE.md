# Post-RC13 Shared Severity UX Gate

## Purpose

Define the durable acceptance contract for the shared severity semantics and filtering used by **Overview** and **Intelligence** after RC13 functional acceptance.

This gate improves analytical presentation and filtering only. It does not reopen RC13, create framework mappings, alter source execution authority, change review/share state or satisfy Phase 8 staging evidence by itself.

## Canonical taxonomy

The supported severity values are:

1. `informational`
2. `low`
3. `medium`
4. `high`
5. `critical`

`critical` is a distinct canonical value and must not be silently collapsed into `high`.

## Shared filter contract

Overview and Intelligence represent one severity selection.

A non-default selection must apply consistently to:

- Overview total intelligence KPI;
- Overview new-in-24-hours KPI;
- Overview average confidence;
- Overview intelligence trend;
- Overview severity distribution;
- Overview source/review intelligence aggregates;
- recent canonical intelligence;
- the existing governed intelligence search severity parameter when a search query is active.

The default `Alle severities` selection sends no severity predicate and preserves the accepted RC13 refresh/empty-state lifecycle.

## Canonical data boundary

Dashboard/recent filtering is applied to canonical PostgreSQL `IntelligenceItem` state.

OpenSearch remains the governed search implementation and reuses its existing exact severity term filter. No separate search subsystem is introduced.

Connector health remains **operational and unfiltered** because connector health is not an intelligence severity property. The API contract exposes that distinction explicitly.

## Visual semantics

Severity presentation must remain accessible and non-colour-only:

| Severity | Semantic colour intent | Required non-colour meaning |
|---|---|---|
| informational | neutral / blue-grey | visible label and accessible name |
| low | green | visible label and accessible name |
| medium | amber / yellow | visible label and accessible name |
| high | red | visible label and accessible name |
| critical | distinct deep/high-severity red treatment | visible label and accessible name |

The UI must provide text labels and/or symbols in cards, legends, charts and table alternatives. Colour alone is insufficient.

## Filtered empty-state contract

If no records match a selected severity:

- KPI totals reflect zero for that filtered slice;
- recent intelligence explicitly states that no records match the selected severity;
- active search explicitly states that no results match the selected severity;
- unrelated records from another severity must not be shown as fallback;
- zero-result visualizations must remain truthful empty states.

## Browser/session behavior

- both selectors remain synchronized;
- the selected value is a non-secret UI preference scoped to `sessionStorage`;
- clearing the filter returns both surfaces to `Alle severities`;
- a persisted non-default value may trigger a filtered refresh after page load;
- a new/default `all` browser session must preserve the accepted RC13 initial refresh lifecycle;
- existing navigation, source operations, Administration and Governance remain usable;
- dedicated browser evidence requires zero page errors and zero console errors.

## Framework mapping boundary

Severity is not evidence of a Normenkader IBP control, MITRE ATT&CK technique or other framework relationship.

The Governance Mapping Registry remains authoritative. Missing mappings remain `UNMAPPED`/`CONTEXT_ONLY`; the severity UI must never infer mappings from severity, titles, tags or free text.

## Security and authority invariants

This feature must preserve:

- server-side RBAC and least privilege;
- human/service-account separation;
- provenance and confidence;
- privacy/data minimization;
- Administration safety controls;
- separate human review and external-share approval;
- no publication authority from filtering, analytics or technical execution.

## Repository evidence contract

Repository acceptance requires one exact PR head to prove both:

1. focused unit/contract evidence for server filtering, canonical taxonomy, composition and non-colour semantics;
2. a Google Chrome browser journey showing shared Overview/Intelligence filtering, search composition, truthful empty states, explicit critical treatment and zero browser page/console errors.

The fail-closed aggregate gate must require both evidence classes to succeed.

## External evidence boundary

Green repository evidence proves only this implementation contract. It does not establish:

- real staging deployment parity;
- production accessibility/UX acceptance;
- independent penetration-test assurance;
- formal production approval.

The enhancement can be credited to Phase 8 only when separately demonstrated against the accepted immutable staging deployment identity.
