# RC7.9 Connector Timeout and Cancellation Gate

Status: `CI_VALIDATION_PENDING`

## Control objective

Prove that a slow or hung upstream connector invocation is bounded by an explicit timeout budget, that timeout/cancellation is scoped to the affected connector, that operational provenance remains attached to the decision, and that no timeout or successful fetch state can imply publication approval.

## Required evidence

- positive timeout budgets are enforced;
- connector ID, run ID and source URI are mandatory operational provenance;
- operations that complete within budget return a non-publishing execution decision;
- operations exceeding budget fail closed as `timeout_budget_exhausted`;
- the timed-out connector task is cancelled;
- timeout of one connector does not cancel an independent connector;
- scheduler/shutdown cancellation is re-raised rather than converted into connector success;
- every timeout decision retains `publish_approved=false`;
- dedicated GitHub Actions execution is observable and retains JUnit and JSON evidence;
- required RC4/RC6/RC7 regression gates succeed on the exact PR head before acceptance.

## Current implementation evidence

Branch `rc7-9-connector-timeout-cancellation` contains:

- `backend/dtmo/connectors/timeout.py`;
- `backend/tests/test_rc7_connector_timeout.py`;
- `.github/workflows/connector-timeout.yml`.

The dedicated workflow is configured to retain `connector-timeout-evidence`, including the timed-out connector provenance, cancellation observation, an independently completing connector, and `publish_approved=false` for both decisions.

No PASS is claimed until GitHub Actions has actually executed on the exact PR head and the retained evidence has been inspected.

## Provider and threat-intelligence context

The NVD states that its API is provided on an `as-available` basis and does not warrant uninterrupted access. Its current developer guidance also enforces request-rate limits and recommends deliberate spacing between requests. These conditions reinforce the need for client-side bounded upstream execution but do not close the external credential, provider-limit, licence or terms gates in issue #1.

A current CVE/threat-intelligence review found no objective-specific CVE that changes the timeout control design. Vulnerability content remains governed by the existing provenance, freshness, replay, quarantine and human-approval controls.

## Acceptance rule

`PASS` is valid only for an exact PR head on which the dedicated timeout gate and all required RC4/RC6/RC7 regression gates have actually succeeded, with retained timeout evidence inspected. Queued, configured, missing or unexecuted workflows are not PASS.
