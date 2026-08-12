# DTMO Finding and Remediation Register

## Purpose

This register defines the authoritative structure for findings produced by independent assurance, penetration testing, environment validation or other formal assessment. It begins empty because no finding may be invented before an assessment produces it.

## Status model

`NEW` → `TRIAGED` → `REMEDIATION_PLANNED` → `REMEDIATED` → `RETEST_PENDING` → `VERIFIED_CLOSED`

Alternative controlled outcomes are `ACCEPTED_RISK`, `DUPLICATE` and `NOT_APPLICABLE`. Risk acceptance requires the authority and expiry/review conditions defined by DTMO risk governance.

## Register

| ID | Source | Severity | Finding | Affected identity | Owner | Status | Remediation / disposition | Retest evidence |
|---|---|---|---|---|---|---|---|---|
| — | — | — | No independent-assurance findings recorded yet | — | — | — | — | — |

## Required finding fields

Each real finding must preserve:

- assessor/source and report reference;
- severity and supporting rationale;
- affected deployment/release/component;
- description and demonstrated impact;
- evidence location/classification;
- accountable remediation owner;
- target date where applicable;
- remediation or risk-treatment decision;
- code/configuration change identity where applicable;
- retest result and assessor evidence where required;
- closure authority and date.

## Release interaction

Critical or high-impact unresolved findings are production blockers unless an explicitly authorized governance rule permits a different treatment. A merged fix is not automatically a closed finding: closure requires the evidence defined by the assessment disposition, including independent retest where required.

## Sensitive evidence

Do not commit exploit payloads, credentials or sensitive assessor evidence to this Markdown register when doing so would expand exposure. Store restricted evidence in the approved controlled location and record only the reference needed for traceability.
