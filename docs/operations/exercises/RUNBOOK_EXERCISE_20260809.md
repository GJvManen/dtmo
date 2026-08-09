# DTMO Controlled Runbook Exercise — 2026-08-09

## Purpose

Execute a bounded, synthetic technical rehearsal of the accepted RC10.9 incident runbooks. This exercise uses no production data, credentials, external communications, destructive actions or publication authority.

## Exercise method

The exercise is scenario-driven and machine-verifiable. Each scenario must demonstrate: alert recognition, severity classification, correlation/evidence capture, reversible containment, security/privacy branching, known-good recovery validation, communication approval, closure criteria and residual-risk handoff.

This is a **controlled synthetic technical exercise**, not a substitute for human on-call handover, stakeholder tabletop participation, production communications testing or external assurance.

## Roles used in the exercise

- Incident Commander
- Operations Lead
- Security Lead
- Service/Data Owner
- Communications/Privacy approver

Human share approval remains mandatory and cannot be exercised by connectors, service accounts, observability components or the technical responder drafting a status update.

## Scenario 1 — API elevated 5xx

**Inject:** `dtmo_api_error_alert_active=1` after sustained 5xx responses.

Expected decisions:

1. classify as SEV-2 unless compromise/integrity evidence raises severity;
2. correlate request/correlation/trace telemetry without copying raw request bodies or query strings;
3. preserve relevant logs before restart/redeploy;
4. use reversible traffic reduction or rollback rather than destructive repair;
5. validate sustained non-5xx recovery and dependency health;
6. require human approval before broad internal/external status publication;
7. record residual cause/ownership before closure.

## Scenario 2 — connector/source degradation

**Inject:** `dtmo_connector_alert_active=1` with stale/failing source activity.

Expected decisions:

1. classify source scope and freshness impact;
2. preserve provenance and quarantine malformed/untrusted records;
3. pause only the affected producer/connector where possible;
4. do not fabricate, backfill or publish unverifiable source claims;
5. recover after controlled canary/replay/freshness validation;
6. preserve human review/share approval;
7. document unresolved source risk and owner.

## Scenario 3 — search-health red/unreachable

**Inject:** `dtmo_search_health_alert_active=1` with red/unreachable cluster status.

Expected decisions:

1. treat search results as potentially incomplete;
2. separate search-plane degradation from primary-system integrity;
3. preserve bounded diagnostics without index contents, queries or identities;
4. avoid destructive index repair until recovery evidence is captured;
5. validate green/yellow stability and representative reads before closure;
6. communicate limitations only through approved channels;
7. record follow-up ownership.

## Scenario 4 — storage-integrity alert

**Inject:** `dtmo_storage_integrity_alert_active=1` after checksum/provenance mismatch.

Expected decisions:

1. classify as SEV-1 when material integrity loss or compromise is suspected;
2. quarantine affected objects/flows and preserve immutable evidence;
3. do not overwrite or repair the questionable evidence in place;
4. restore only from a known-good immutable source/backup;
5. validate checksum, provenance and application-level integrity after recovery;
6. require approved communication for any disclosure;
7. retain evidence location, residual risk and accountable owner.

## Exercise result contract

A scenario passes only when every required decision above is present and governance invariants remain true:

- RBAC unchanged;
- separation of duties unchanged;
- publication/share approval unchanged;
- no production data or credentials used;
- evidence/provenance preserved;
- recovery requires objective validation, not alert clearance alone.

## Threat-informed basis

CISA's Cybersecurity Tabletop Exercise Program provides facilitator/evaluator and after-action templates; CISA also recommends exercising incident-response plans and realistic scenarios. The exercise therefore records scenario objectives, expected decisions, evidence and residual gaps rather than equating document existence with operational readiness.

Provenance reviewed 2026-08-09:

- CISA CTEP Package Documents: https://www.cisa.gov/resources-tools/resources/ctep-package-documents
- CISA Cybersecurity Scenarios: https://www.cisa.gov/resources-tools/resources/cybersecurity-scenarios
- CISA #StopRansomware Guide: https://www.cisa.gov/stopransomware/ransomware-guide

Confidence: high for these first-party exercise/incident-response principles.

## Residual gaps after this exercise

- human on-call handover and operational ownership acceptance;
- production contact/escalation roster approval;
- human tabletop timing/decision-quality evidence;
- production/staging communications-path testing;
- external assurance gates in issue #1.
