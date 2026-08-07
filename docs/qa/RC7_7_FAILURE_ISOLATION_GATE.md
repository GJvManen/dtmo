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

## Observed implementation-head evidence

Implementation/documentation head `3c263f71e62c5a82b5160071689d58c76f89e7f3` executed RC7 Connector Failure Isolation Gate run `31184266766` successfully.

Retained artifact:

- artifact ID: `8996062460`;
- digest: `sha256:06466abc69ecb630941c17ade18ff88e661101103e88452f17e3b9b557f519f7`;
- expired: false at inspection;
- JSON decision: `pass`;
- JUnit: 6 tests, 0 failures, 0 errors, 0 skipped;
- failure threshold: 3;
- observed failure events: 3;
- failing connector decision: `allowed=false`, reason `circuit_open`, health `isolated`;
- independent connector decision: `allowed=true`;
- post-isolation recovery decision: `allowed=true`, reason `recovery_probe`;
- health events and all execution decisions: `publish_approved=false`.

The artifact was independently downloaded and inspected during RUN-20260807-060 rather than inferred from workflow configuration.

At the same head, RC7 Live Connector Canary, Connector State, Freshness, Payload Provenance, Connector Contract and Connector Replay had completed successfully at the latest check. RC4 Quality, RC6 OpenSearch Recovery and RC6 Multi-store Recovery were still in progress, so RC7.7 remained `CI_VALIDATION_PENDING` and no merge was permitted.

## Threat and incident context

The implementation is intentionally connector-local. CISA's K-12 cybersecurity reporting documents historical vendor incidents with broad downstream school impact, including an incident in which one hosting vendor outage affected thousands of school websites. This supports failure-domain isolation as a high-confidence resilience requirement for education-sector intelligence services. CISA also recommends isolating affected systems and maintaining continuity during cyber incidents.

Sources reviewed on 2026-08-07:

- CISA, *Protecting Our Future: Partnering to Safeguard K-12 Organizations from Cybersecurity Threats*, https://www.cisa.gov/sites/default/files/2023-01/K-12report_FINAL_V2_508c_0.pdf — confidence: high (primary government source; historical incident context).
- CISA, *Cyber Risk to Public Safety: Ransomware*, https://www.cisa.gov/sites/default/files/2023-02/CISA%20Cyber%20Risks%20to%20Public%20Safety%20Ransomware_9.29.20%20-%20FINAL%20%28508c%29_0.pdf — confidence: high (primary government resilience guidance).

No connector-specific new CVE or vendor advisory changes the bounded objective of this run; production source credentials, provider rate limits, licences and provider acceptance remain external gates in issue #1.

## Acceptance rule

RC7.7 may be marked `PASS` only after the exact pull-request head has executed this gate and all required RC4/RC6/RC7 regression workflows successfully, and the retained failure-isolation artifact has been independently inspected. Documentation changes move the PR head and therefore require fresh exact-head CI. Until then the status remains `CI_VALIDATION_PENDING`.
