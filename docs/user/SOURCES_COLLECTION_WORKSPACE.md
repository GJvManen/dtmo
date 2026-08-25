# Sources & Collection workspace

The canonical **Sources & Collection** workspace is the governed operator surface for code-reviewed source profiles, registered connectors and collection control.

## Access

The workspace requires an authenticated DTMO session with `manage:connectors`. Registry changes and explicit operator execution remain additionally restricted by the server to a human administrator. A hidden or disabled browser control is never an authorization boundary.

## Catalog and registration

The catalog lists code-reviewed source profiles and their execution status. **Bootstrap supported catalog** idempotently registers supported profiles that do not already exist. New bootstrap registrations are disabled by default; registration does not mean the source is trusted, healthy or collecting.

## Activation and automatic collection

Activation is the persisted administrative decision that a registered source may collect. Once the application live-connector scheduler is enabled, a persisted source is eligible for automatic collection only when all of the following remain true:

- the source itself is enabled;
- it maps to a code-reviewed catalog entry whose execution status is `supported`;
- its execution adapter is registered;
- a credentialed adapter has a logical server-side secret reference;
- the source is not in fail-closed connector isolation; and
- its own persisted `interval_seconds` has elapsed since the most recent recorded run.

The reconciliation job runs immediately when the live scheduler starts and then checks eligibility every 60 seconds. It does **not** turn disabled sources on, execute research-only catalog entries, bypass missing credential references or override connector isolation. Built-in CISA KEV remains on its dedicated connector execution path.

Automatic execution uses the same governed source adapter, canonical ingestion, provenance, connector-state and alerting paths as explicit collection. Each automatic run is recorded with the service identity `service:source-scheduler` and the audit action `source.auto-run`.

## Bounded actions

**Validate** checks the stored endpoint against DTMO's governed source policy. Runtime execution still re-resolves DNS and applies destination, redirect, TLS and response-bound controls.

**Test** performs a bounded non-ingesting execution. A successful test means only that the recorded test completed; it does not authorize activation, sharing or publication.

**Run** remains available as an explicit collection action for an authorized human administrator. Completed records are sent through DTMO's governed ingestion and provenance path. Repeated connector failures can place a source in fail-closed isolation, in which case both explicit and automatic execution respect the existing recovery controls.

## Credentials

The browser never receives upstream secret values. Credentialed source adapters use logical server-side secret references. The automatic scheduler only observes whether the required reference exists; actual credential resolution happens inside the governed server-side executor. A displayed authentication mode or `secret_ref` is metadata, not a credential value.

## Interpretation and authority boundary

Automatic scheduling proves only that DTMO attempted or completed the recorded collection action according to persisted configuration. It is not a provider-health claim and does not establish source truth, local compromise, review completion, remediation, external-share approval, publication authority, production-equivalent operation or production authorization.

Human review, case, sharing and publication authorities remain separate. Repository CI validates the implementation contract but is not evidence that a particular external source or environment was successfully contacted.
