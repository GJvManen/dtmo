# DTMO Operational Incident Runbooks

These runbooks are the bounded Phase 7 incident-operations baseline for DTMO. They turn existing alerts, structured logs, correlation IDs, trace IDs, recovery controls and human approval boundaries into repeatable operator procedures.

## Scope

Use these runbooks for:

- [API outage or elevated server errors](API_OUTAGE.md)
- [Connector failure or upstream source degradation](CONNECTOR_FAILURE.md)
- [Search-health degradation](SEARCH_HEALTH_DEGRADATION.md)
- [Storage-integrity failure and recovery](STORAGE_INTEGRITY_RECOVERY.md)

These documents do **not** authorize destructive remediation, production publication, disclosure to external parties, or bypass of RBAC/change controls. Human review/share approval remains mandatory and separate from incident handling; **human share approval** is never granted to technical responders, connectors, observability components or service accounts by incident status alone.

## Common incident roles

- **Incident Commander (IC):** owns severity, scope, decisions, timeline and handoff.
- **Operations Lead:** performs approved technical containment/recovery and records evidence.
- **Security Lead:** assesses compromise indicators, credential exposure, exfiltration and evidence-preservation needs.
- **Service/Data Owner:** validates business impact and recovery acceptance.
- **Communications/Privacy approver:** approves any external/internal disclosure where required. Technical responders cannot self-approve publication.

One person may temporarily hold multiple roles in a small response, but approval of external sharing must remain separated from the person drafting the communication whenever feasible.

## Severity baseline

- **SEV-1:** confirmed or strongly suspected compromise, material data-integrity loss, widespread unavailability, or safety/privacy-critical impact.
- **SEV-2:** significant service degradation, repeated alert condition, connector/source outage affecting analysis, or recoverable search/storage impairment without confirmed compromise.
- **SEV-3:** isolated/recoverable fault with limited impact and no evidence of compromise or integrity loss.

Escalate severity when scope, confidentiality, integrity or availability impact increases. Never downgrade solely because an alert clears automatically.

## Evidence and privacy rules

Record only what is needed to reconstruct decisions and technical state: UTC timestamps, alert name/metric, bounded route/connector/queue/storage/search identifiers, correlation ID, trace ID where available, deploy/change identifier, operator actions and validation results. Do not paste credentials, bearer tokens, raw request bodies, student/person data, full query strings, object payloads or unnecessary sensitive diagnostics into tickets or chat.

Preserve relevant logs and immutable/raw evidence before destructive changes when compromise is suspected. Maintain chain-of-custody/provenance for exported evidence.

## Universal response sequence

1. **Acknowledge and classify.** Record alert/time, assign IC, estimate scope and severity.
2. **Correlate.** Use correlation/trace IDs and the DTMO Operations dashboard to separate application, connector, queue, search and storage symptoms.
3. **Protect evidence.** Preserve logs/receipts before restarts, deletion or restoration when security/integrity is in question.
4. **Contain safely.** Prefer reversible isolation, traffic reduction, credential/session revocation and producer pausing over destructive action.
5. **Recover from a known-good state.** Follow the specific runbook and existing recovery procedures; do not make unverifiable in-place repairs to evidence.
6. **Validate.** Require objective health/integrity checks and a stable observation period; an alert clearing alone is insufficient.
7. **Communicate with approval.** Draft status with facts/confidence/unknowns. External or broad internal sharing requires the applicable human approver.
8. **Close or hand over.** Record residual risk, follow-up tickets, evidence locations and ownership.

## Threat-informed rationale

Education institutions have historically experienced ransomware-driven disruption and theft/extortion of student data. CISA/FBI reporting on education-sector PaperCut exploitation also shows how an exposed enterprise service can become an entry point for remote tooling, exfiltration and encryption. The runbooks therefore prioritize rapid scope determination, credential/account review, evidence preservation, containment, known-good recovery and explicit communication approval.

Provenance reviewed 2026-08-09:

- CISA, *Cyber Threats to K-12 Remote Learning Education*: https://www.cisa.gov/stopransomware/cyber-threats-k-12-remote-learning-education
- CISA, *#StopRansomware Guide*: https://www.cisa.gov/stopransomware/ransomware-guide
- CISA/FBI, *Malicious Actors Exploit CVE-2023-27350 in PaperCut MF and NG*: https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-131a

Confidence: **high** for the response principles above; these sources document observed education-sector disruption/exfiltration and established incident-response guidance. No attribution claim is made for any future DTMO incident.

## Exercise boundary

This baseline is not considered exercised merely because its document-validation workflow passes. Phase 7 still requires a controlled runbook exercise and operational ownership/on-call handover evidence.
