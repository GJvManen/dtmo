# RC10.9 Operational Runbooks Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate a bounded incident-response runbook baseline for API outage, connector failure, search-health degradation and storage-integrity/recovery, tied to existing DTMO operational signals and preserving security, privacy, provenance and human publication approval.

## Required exact-head evidence

Acceptance requires all of the following on one final PR head:

- common incident roles and SEV-1/2/3 severity guidance are documented;
- API outage runbook references `dtmo_api_error_alert_active`;
- connector failure runbook references `dtmo_connector_alert_active` and preserves provenance/freshness controls;
- search degradation runbook references `dtmo_search_health_alert_active` and treats red/unreachable search results as potentially incomplete;
- storage recovery runbook references `dtmo_storage_integrity_alert_active`, quarantine and known-good restoration;
- each service runbook defines trigger, immediate checks, containment, recovery, security/privacy escalation, communication and closure criteria;
- evidence preservation and correlation/timeline capture are defined;
- incident records exclude credentials, raw request/payload data and unnecessary personal data;
- RBAC, separation of duties, provenance and human share approval are unchanged;
- dedicated `RC10 Operational Runbooks Gate` succeeds and retains exact-head JUnit/log/JSON evidence;
- every registered workflow succeeds on the exact final head.

## Threat/historical incident boundary

CISA education-sector ransomware material and CISA/FBI PaperCut exploitation reporting were reviewed to ensure the runbooks account for service disruption, credential/account compromise, data exfiltration, evidence preservation and controlled recovery. These sources inform response priorities; they do not imply any current DTMO compromise or future threat-actor attribution.

## Claim boundary

This gate does **not** claim:

- the runbooks have been exercised;
- on-call handover or operational ownership is accepted;
- production communications/escalation contacts are approved;
- Phase 7 is complete;
- Phase 6 assistive-technology evidence is complete;
- any issue #1 external production gate is complete.

## Exactly one next priority

Accept only after complete exact-head workflow success and independent retained `operational-runbooks-evidence` inspection.
