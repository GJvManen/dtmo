# RC7.7 Connector Failure Isolation Gate

Status: `CI_VALIDATION_PENDING`

## Objective

Evidence that repeated upstream connector failures are observable and bounded by a connector-local circuit, that isolation cannot cascade to unrelated connectors, and that health/failure/recovery state never grants publication approval.

## Controls under test

- Connector runtime health is persisted per `connector_id`.
- Repeated failures reach the configured threshold and open only that connector's circuit.
- An open circuit produces a fail-closed execution decision.
- An unrelated connector remains independently executable.
- Isolation expiry permits a recovery probe under normal scheduler cadence.
- Health decisions and health events always retain `publish_approved=false`.
- Missing execution evidence cannot be interpreted as success.

## Evidence workflow

`.github/workflows/connector-failure-isolation.yml` runs `backend/tests/test_rc7_connector_failure_isolation.py`, emits JUnit evidence and a deterministic JSON evidence record, and retains both in the `connector-failure-isolation-evidence` artifact for 30 days.

The gate job uses `if: always()` and fails unless the evidence-producing job actually succeeds.

## Threat and incident context

The implementation is intentionally connector-local. CISA's K-12 cybersecurity reporting documents historical vendor incidents with broad downstream school impact, including an incident in which one hosting vendor outage affected thousands of school websites. This supports failure-domain isolation as a high-confidence resilience requirement for education-sector intelligence services. CISA also recommends isolating affected systems and maintaining continuity during cyber incidents.

Sources reviewed on 2026-08-07:

- CISA, *Protecting Our Future: Partnering to Safeguard K-12 Organizations from Cybersecurity Threats*, https://www.cisa.gov/sites/default/files/2023-01/K-12report_FINAL_V2_508c_0.pdf — confidence: high (primary government source; historical incident context).
- CISA, *Cyber Risk to Public Safety: Ransomware*, https://www.cisa.gov/sites/default/files/2023-02/CISA%20Cyber%20Risks%20to%20Public%20Safety%20Ransomware_9.29.20%20-%20FINAL%20%28508c%29_0.pdf — confidence: high (primary government resilience guidance).

No connector-specific new CVE or vendor advisory changes the bounded objective of this run; production source credentials, provider rate limits, licences and provider acceptance remain external gates in issue #1.

## Acceptance rule

RC7.7 may be marked `PASS` only after the exact pull-request head has executed this gate and all required RC4/RC6/RC7 regression workflows successfully, and the retained failure-isolation artifact has been independently inspected. Until then the status remains `CI_VALIDATION_PENDING`.
