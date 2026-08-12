# Governed Source Registry Release Gate

**Status:** `PASS` for the accepted source-registry backend contract

## Objective

Define the security and governance contract for DTMO source registration and lifecycle management.

This gate covers the canonical source-registry control plane. Source execution safety and the end-to-end intelligence pipeline are covered by their related gates.

## Required controls

Source-registry mutations must preserve:

- `manage:connectors` server-side permission;
- human administrator authority for registry mutations;
- no use of the human admin mutation surface by service accounts;
- constrained source IDs and supported registry source types;
- HTTPS public-host endpoint validation;
- rejection of local/internal hostnames, non-global literal IPs, embedded URL credentials and non-default HTTPS ports;
- logical secret references only, never raw secret values;
- explicit enabled state, reliability and poll interval;
- persistent audit events with actor/request correlation;
- no change to review/share/publication authority.

## Current backend capability

The accepted backend provides governed operations for:

- listing sources;
- creating source definitions;
- updating source definitions;
- validation;
- enabled/disabled state;
- reliability and interval management;
- logical `secret_ref` configuration;
- catalog bootstrap.

Registered sources default to disabled when introduced through the catalog bootstrap flow.

## Current UI boundary

The canonical `Sources & Catalog` area exposes governed source/catalog operations, but the accountable owner has identified a UX gap: there is not yet a complete professional manual-source onboarding journey in the canonical interface.

This is a **product UX enhancement**, not an absence of the underlying registry API. The enhancement must reuse the canonical registry and audit model instead of introducing a parallel source-management mechanism.

## Security boundary

Registry validation establishes that configuration is syntactically/policy compliant; it does not by itself establish:

- source trustworthiness;
- legal authorization to automate/redistribute material;
- successful live execution;
- provider availability;
- production credential approval;
- external-share/publication authority.

Safe remote execution additionally requires the source-execution network, response, normalization, provenance and persistence contracts.

## Evidence requirements for future changes

Any registry change must include applicable evidence for:

1. RBAC/human-service-account separation;
2. URL/SSRF configuration validation;
3. secret-reference handling;
4. migration/data-model integrity where changed;
5. persistent audit behavior;
6. UI/API wiring where changed;
7. preservation of review/share authority boundaries;
8. complete exact-head CI on the final PR head.

A new commit invalidates earlier exact-head evidence.

## Claim boundary

This gate's current PASS applies to the accepted backend registry/control-plane contract. The planned canonical manual onboarding UI requires separate acceptance evidence before it can be claimed complete.
