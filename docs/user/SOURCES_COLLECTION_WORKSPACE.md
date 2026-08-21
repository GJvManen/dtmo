# Sources & Collection workspace

The canonical **Sources & Collection** workspace is the governed operator surface for code-reviewed source profiles, registered connectors and explicit collection actions.

## Access

The workspace requires an authenticated DTMO session with `manage:connectors`. Registry changes and execution remain additionally restricted by the server to a human administrator. A hidden or disabled browser control is never an authorization boundary.

## Catalog and registration

The catalog lists code-reviewed source profiles and their execution status. **Bootstrap supported catalog** idempotently registers supported profiles that do not already exist. New bootstrap registrations are disabled by default; registration does not mean the source is trusted, healthy or collecting.

## Bounded actions

**Validate** checks the stored endpoint against DTMO's governed source policy. Runtime execution still re-resolves DNS and applies destination, redirect, TLS and response-bound controls.

**Test** performs a bounded non-ingesting execution. A successful test means only that the recorded test completed; it does not authorize activation, sharing or publication.

**Run** is an explicit collection action. Completed records are sent through DTMO's governed ingestion and provenance path. Repeated connector failures can place a source in fail-closed isolation, in which case execution is refused until the existing recovery controls permit it.

## Credentials

The browser never receives upstream secret values. Credentialed connectors use server-side secret references and code-reviewed adapter profiles. A displayed authentication mode or `secret_ref` is metadata, not a credential value.

## Interpretation

Connectivity, validation, a successful test, or successful ingestion must never be interpreted as proof of source truth, local compromise, review completion, external-share approval, publication authority, production-equivalent operation or production authorization. Human review/share/case authorities remain separate.

Phase 10 remains **NO-GO / BLOCKED — PLATFORM INDUSTRIALISATION REQUIRED**. Repository CI is non-production evidence.
