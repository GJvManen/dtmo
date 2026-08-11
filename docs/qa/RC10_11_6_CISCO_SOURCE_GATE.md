# RC10.11.6 Cisco Security Advisory Source Gate

Status: `PENDING_CI`

## Objective

Connect Cisco Security Advisories to the unified DTMO console using the official Cisco PSIRT OpenVuln API v2 without storing bearer credentials in source control or the source registry.

## Accepted implementation boundary

- canonical API base is `https://apix.cisco.com/security/advisories/v2`
- execution profile is `cisco-openvuln-v2`
- the catalog stores only `env:CISCO_OPENVULN_TOKEN`; the credential value remains external
- runtime execution uses `/latest/25?summaryDetails=true&productNames=true`
- requests retain HTTPS-only URL validation, DNS re-resolution, global-address rejection, pinned TLS, redirect rejection and 5 MiB response bounds
- normalization requires a Cisco advisory ID, title and HTTPS publication URL
- raw Cisco advisory JSON is retained as provenance
- absence of the runtime credential fails closed and does not downgrade to anonymous scraping
- ingestion does not grant review, publication or share approval authority

## Required evidence before PASS

1. exact-head RC4 Quality Gate completes successfully
2. source execution contract tests pass
3. Cisco adapter normalization and fail-closed secret tests pass
4. container and staging-emulator runtime gates pass
5. connector provenance and state gates remain green
6. source connection matrix reflects Cisco as connected only after exact-head acceptance

## Claim boundary

This gate accepts the Cisco adapter and generic environment-backed secret-reference dispatcher only. It does not claim production secrets-manager acceptance, possession of a real Cisco credential, or real-staging provider acceptance. Those remain external release evidence.
