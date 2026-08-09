# RC10.10 Operational Runbook Exercise Gate

## Decision

`CI_VALIDATION_PENDING`

## Objective

Validate a bounded synthetic technical exercise across the accepted API outage, connector failure, search-health degradation and storage-integrity/recovery runbooks while preserving security, privacy, provenance, separation of duties and human share approval.

## Required exact-head evidence

Acceptance requires all of the following on one final PR head:

- all four scenarios are present and bound to existing alert signals;
- each scenario includes classification, evidence capture, containment, recovery validation, communication approval and residual-risk handoff;
- recovery requires known-good state and objective validation rather than alert clearance alone;
- no production data or credentials are used;
- no destructive remediation or external communications are executed by the exercise;
- RBAC and publication/share approval are unchanged;
- the exercise explicitly does not claim human tabletop completion, on-call handover or operational ownership acceptance;
- dedicated `RC10 Operational Runbook Exercise Gate` succeeds and retains exact-head JUnit/log/JSON evidence;
- every registered workflow succeeds on the exact final head.

## Current CI evidence

PR #97 exact head `1862b1c4e9e768da82baef3470464845cadf3967` completed **43/44 workflows successfully**. `RC10 Operational Runbook Exercise Gate` run `31331042196` failed even though its scenario tests passed **5/5** and evidence was produced.

The deterministic defect was in `Validate evidence contract`: `assert all(e["controls"].values())` incorrectly treated the intentionally false safety controls `production_data_used=false` and `production_credentials_used=false` as failures. Artifact `9042942892` belongs to that failed head and cannot be used for acceptance.

RUN-143 corrects the validator without changing scenario results or governance boundaries. Required-positive controls are asserted `True`; the two safety controls are asserted `False`; claim-boundary values must remain all false. No workflow or test is bypassed.

The failed head is **not accepted**. All 44 workflows and retained evidence must regenerate on one new exact final head.

## Threat/exercise boundary

CISA CTEP and cybersecurity-scenario guidance reviewed in RUN-142 remains applicable. These sources support scenario-driven exercises and after-action capture. They do not make this synthetic CI exercise equivalent to a human tabletop or production operational acceptance.

## Claim boundary

This gate does **not** claim:

- human tabletop participation or timing evidence;
- on-call handover is complete;
- operational ownership/escalation is accepted;
- production contact paths are approved/tested;
- Phase 7 is complete;
- any issue #1 external production gate is complete.

## Exactly one next priority

Verify complete fresh exact-head workflow success and independently inspect regenerated `operational-runbook-exercise-evidence`; accept and merge PR #97 only if both are complete and internally consistent.
