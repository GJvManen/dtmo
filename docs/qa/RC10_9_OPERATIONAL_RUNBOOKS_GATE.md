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
- RBAC, separation of duties, provenance and **human share approval** are unchanged and explicitly documented;
- dedicated `RC10 Operational Runbooks Gate` succeeds and retains exact-head JUnit/log/JSON evidence;
- every registered workflow succeeds on the exact final head, including the aggregate `RC4 Quality Gate`.

## Current CI evidence

PR #96 head `42d7104915a5e424e9cebc2e4f0a093cf7948f94` completed **42 of 43 workflows successfully**. The dedicated `RC10 Operational Runbooks Gate` succeeded, but the release-critical `RC4 Quality Gate` failed in its full pytest step.

Workflow run `31329981268`, job `93286565269`, failed in `backend/tests/test_rc10_9_operational_runbooks.py::test_runbook_set_exists_and_has_common_response_controls`. The test requires the canonical phrase `human share approval`; the runbook index used `Human review/share approval`, so the machine-checked governance contract was incomplete. Lint and mypy both passed.

RUN-141 remediates the documentation contract, not the test. The index now explicitly states that **human share approval** is never granted to technical responders, connectors, observability components or service accounts by incident status alone. No test, workflow or governance control was weakened.

The failed head is **not accepted**. All workflows and retained `operational-runbooks-evidence` must rerun on the new exact head; prior-head artifact evidence cannot be reused.

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

Verify the complete fresh exact-head workflow matrix and regenerated retained `operational-runbooks-evidence`; accept and merge PR #96 only if all evidence is complete and internally consistent.
