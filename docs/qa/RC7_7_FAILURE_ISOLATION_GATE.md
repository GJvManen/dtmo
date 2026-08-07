# RC7.7 Connector Failure Isolation Gate

Status: `PASS`

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

## Final exact-head evidence

PR #34 exact head `4d17dfc7a9cd7f0bbc155fa0c42770ba34535ae2` passed all required workflows: RC4 Quality #335, RC6 OpenSearch #87, RC6 Multi-store #77, RC7 State #40, Canary #68, Contract #39, Payload Provenance #30, Replay #11, Freshness #7 and Failure Isolation #3.

Retained `connector-failure-isolation-evidence` artifact `8996123528` was independently downloaded and inspected. Digest: `sha256:d5b53752e7cd81ba8790f0f3f8a3c64e23ffa7f12cfd4962896e30b95f9fe20f`. It was not expired. JSON recorded `decision=pass`, failure threshold 3, three failure events, isolated connector `allowed=false` with reason `circuit_open`, independent connector `allowed=true`, recovery probe `allowed=true`, and `publish_approved=false` for every health event and execution decision. JUnit recorded 6 tests with 0 failures, 0 errors and 0 skips.

PR #34 was merged with expected-head protection as `6f033c57e2b143172347a88ad1c0213915226ac1`.

## Threat and incident context

RUN-20260807-060 recorded high-confidence CISA K-12 historical incident and resilience context supporting connector-local failure-domain isolation. No new connector-specific CVE or vendor advisory changed this bounded acceptance decision. Production credentials, provider rate limits, licences, terms and provider acceptance remain external gates in issue #1.

## Acceptance decision

`PASS`. Exact-head workflow execution, retained evidence inspection and protected merge are complete. This does not complete Phase 4 or any external production gate.
