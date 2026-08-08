# Phase 4 Live Connector Reliability and Provenance Acceptance

Status: `CI_VALIDATION_PENDING`

## Scope

This gate closes Phase 4 only after both evidence classes are satisfied: previously accepted RC7.1–RC7.9 CI/runtime evidence and external/manual verification of the remaining live-connector production conditions.

## Internal evidence already accepted

RC7.1 through RC7.9 established observable canary execution, governed connector contracts, persistent connector state, payload provenance, replay protection, freshness handling, failure isolation, bounded retry/backoff, timeout/cancellation budgets, quarantine behavior and mandatory `publish_approved=false` throughout connector-controlled states. RUN-20260807-065 verified the latest exact-head RC7.9 execution and retained connector-timeout evidence before PR #36 merged.

## External/manual evidence

On 2026-08-08 the project owner explicitly attested that production credential suitability, provider-enforced rate/usage limits, applicable licence/terms obligations and provider-specific production acceptance evidence have been verified.

Evidence classification: `EXTERNAL_MANUAL_ATTESTATION`.

Confidence: `HIGH` for the fact of owner attestation; underlying provider/environment materials remain external and are not represented as CI artifacts.

## Pending acceptance condition

The substantive Phase 4 connector requirements are satisfied. Final repository acceptance remains fail-closed until the exact head containing this acceptance record executes the required GitHub Actions gates successfully. Missing, queued, cancelled or unexecuted workflows are not PASS.

This gate does not close unrelated issue #1 requirements such as independent penetration testing, general staging/production deployment acceptance, load/stress testing, full backup/restoration, OpenSearch production hardening, secrets-manager replacement or operational acceptance.

## Governance invariants

Connectors cannot publish without human review; review and share approval remain separated; connector-controlled state never implies publication approval; provenance/confidence/raw evidence remain mandatory; secret values must not enter evidence.

## Next gate

Inspect exact-head CI for the acceptance-record branch. Only after successful execution may Phase 4 be marked `PASS` and Phase 5 begin.