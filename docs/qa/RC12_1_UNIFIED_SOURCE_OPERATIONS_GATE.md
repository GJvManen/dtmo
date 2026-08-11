# RC12.1 Unified Source Operations Gate

Status: **PENDING_CI**

## Objective

Make the canonical DTMO unified console the operational administration surface for the complete accepted source catalog instead of requiring operators to switch to separate source-management URLs.

## Accepted implementation scope

- canonical product surface remains `/` and `/ui/console`
- supported catalog sources can be idempotently bootstrapped from the console
- registered sources expose enable/disable control in the same source card
- registered sources expose bounded scheduling interval management (60..86400 seconds)
- registered sources expose governed source validation
- manual run is exposed only when the source is registered, enabled and the source-center contract marks manual execution available
- existing admin APIs, human-admin RBAC, request IDs, audit events, source framework dispatch, isolation and publication approval boundaries remain server-side authoritative
- administration links back into the same source-operations view rather than opening a second management application
- RC11 vendor onboarding is closed in `SOURCE_CONNECTION_MATRIX.md`; all currently catalogued operational vendor sources are CONNECTED

## Explicit non-claims

RC12.1 does not claim:

- production identity-provider acceptance
- production secret-manager acceptance
- live provider availability or SLA
- scheduler/background execution redesign
- completed advanced graphical dashboards
- review or external share approval authority

## Regression evidence required

`backend/tests/test_rc12_unified_source_operations.py` must prove that:

1. bootstrap, PATCH configuration, validation and manual-run endpoints are wired into the unified console;
2. run controls remain unavailable for unregistered or disabled sources;
3. Administration reuses the same shell/source-operations surface;
4. the maintained source matrix contains no remaining vendor `ADAPTER_REQUIRED` or `PENDING_CI` entry after accepted RC11.10 onboarding.

Existing RC10 unified-console, source-framework, connector, RBAC, accessibility and provenance tests remain mandatory regression coverage.

## Release rule

Do not change this gate to PASS and do not merge the PR until the complete exact-head GitHub Actions workflow set is `completed/success`. Any required workflow failure leaves this gate blocked and must be remediated without lowering an existing quality, security, accessibility or coverage threshold.
