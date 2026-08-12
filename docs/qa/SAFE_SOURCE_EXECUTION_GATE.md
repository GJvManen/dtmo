# Safe Registered-Source Execution Gate

**Status:** `PASS` for the accepted source-execution contract

## Objective

Define the fail-closed trust boundary for executing registered external intelligence sources without weakening SSRF protection, provenance, credential handling, canonical persistence or human approval controls.

## Authorization requirements

- Manual source execution requires server-side connector-management authority.
- Human/admin requirements apply where the administrative source surface requires them.
- Disabled sources cannot execute through governed source operations.
- Service-account and human authorities remain separated.
- Source execution never grants review or external-share approval.

## Network and SSRF contract

Registered/generic source execution must preserve the applicable controls for:

- HTTPS-only registered source URLs;
- public/global destinations;
- fresh DNS resolution immediately before connection where the executor requires it;
- rejection of non-global/private/local/reserved destinations;
- protection against DNS rebinding;
- original hostname retention for TLS SNI/certificate verification when connecting to a validated address;
- redirect restrictions for profiles that require direct execution;
- no untrusted environment-proxy redirection of the protected execution path;
- bounded response size and supported content types.

Provider-specific adapters may implement profile-appropriate first-party discovery while remaining bounded to the documented provider trust contract.

## Credential handling

- Credential values are never stored in the source catalog or registry.
- Credentialed sources use approved logical secret references.
- Execution fails closed when a required secret reference cannot be resolved or its reference scheme is unsupported.
- Staging/production identity references must map to approved least-privilege identities.
- Local infrastructure/root credential compatibility exceptions are not valid staging/production source identity patterns.

## Parsing and normalization

Only supported profiles/contracts are normalized into canonical connector records.

The accepted baseline includes provider-specific and shared profiles for vulnerability/advisory sources. Normalization must preserve:

- source identity;
- reliability/context;
- canonical intelligence type;
- canonical URL/reference policy;
- raw upstream evidence/references;
- relevant publication timestamps/context.

Explicit supported aliases may be normalized; unknown canonical intelligence types fail closed.

## Persistence and replay

Normalized records enter the accepted pipeline:

```text
source execution
  -> raw evidence object
  -> canonical normalization/provenance
  -> PostgreSQL durable commit
  -> OpenSearch index/search representation
  -> application visibility
```

Application-level durable success must not be reported before the canonical PostgreSQL transaction completes.

Where the connector contract defines idempotency/replay behavior, repeat execution must not create inconsistent canonical duplicates and may repair supporting derived index state without bypassing canonical truth.

## Operational behavior

Source execution integrates with connector state/freshness/failure-isolation and relevant alerting/observability. Failures must remain diagnosable without leaking raw sensitive credentials or unnecessary payload data.

## Evidence required for changes

Future changes to source execution require applicable coverage for:

- authorization/disabled-state behavior;
- URL/network/SSRF protections;
- credential/secret-reference behavior;
- profile parsing/normalization;
- provenance/raw evidence;
- canonical commit behavior;
- idempotency/replay;
- connector state/failure isolation;
- application visibility;
- complete exact-head CI.

## Claim boundary

This gate does not prove:

- current provider SLA/availability;
- enterprise production egress policy;
- legal/contractual permission to automate restricted sources;
- real Phase 8 staging acceptance;
- independent penetration-test results;
- production go/no-go;
- publication/external-share authority.

Those remain separate evidence/authority classes.
