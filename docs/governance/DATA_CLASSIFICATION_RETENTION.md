# DTMO Data Classification and Retention Model

Last reviewed: **2026-08-16**

## Purpose

This document defines the baseline classification and retention principles for DTMO information. It supports privacy, security, evidence handling and environment governance. Actual statutory, contractual or organizational retention requirements must be applied by the accountable deployment owner where they are stricter or more specific.

## Classification levels

| Level | Description | Examples | Handling expectation |
|---|---|---|---|
| Public | Approved for unrestricted disclosure | Public documentation, approved release notes | May be publicly shared after normal publication controls |
| Internal | Operational/project information not intended for unrestricted publication | Internal runbooks, non-sensitive project status | Authenticated access; minimize unnecessary external distribution |
| Sensitive | Information whose disclosure or alteration could materially affect security, privacy or operations | Detailed threat data, internal architecture details, audit records | Least privilege, controlled storage, logged access where appropriate |
| Restricted | High-impact security/privacy information | Raw credentials, bearer tokens, production secrets, highly sensitive personal/security data | Dedicated secret/protected storage; never repository/documentation evidence |

Classification is based on content and impact, not file location. A repository path does not make Restricted data safe to commit.

## Data categories

### Intelligence records
Normalized threat intelligence with source/provenance metadata. Usually `Internal` or `Sensitive` depending on source, content and deployment context.

### Raw source evidence
Original provider material retained for provenance and reconstruction. Classification follows the most sensitive contained information and source terms.

### Enrichment observables and results

Observables submitted to an external enrichment service may disclose data to the service and, depending on the approved analyzer, to a third-party provider. Classification and handling therefore follow the submitted value, its context and the most restrictive applicable source/TLP/privacy rule.

Phase 11.3 IntelOwl initially permits only governed CVE, IP, domain, URL and cryptographic-hash observables. Email addresses and other generic personal-data observables remain disabled until an explicit privacy/data-processing decision establishes lawful purpose, provider/transfer conditions and retention requirements.

IntelOwl analyzer reports are attributed enrichment evidence. They must retain analyzer/provider provenance and must not be treated as proof of local exposure or compromise merely because an external provider returns a malicious/suspicious verdict.

The governed Phase 11.3 execution slice persists immutable enrichment history in `intelowl_enrichment_records`, linked to the canonical intelligence item. The record retains the IntelOwl job identity, observable type/value, handling decision input, requested analyzers, explicit partial-success state, attributed reports, bounded normalized raw result, requesting human subject and timestamp. Database constraints force `external_share_authorized=false` and `local_compromise_proven=false`; persistence is evidence context, not publication authority or compromise proof.

Because the durable record includes the submitted observable and provider result, its classification is at least as restrictive as the submitted observable/context and may become more restrictive when analyzer output introduces sensitive data. The current implementation does not establish an independent fixed retention duration; deployment policy must apply the bounded lifecycle described below before production authorization.

### Identity and authorization data
Principal identifiers, roles, assignments and audit-relevant authorization state. Generally `Sensitive`.

### Audit and operational telemetry
Actor/action context, correlation IDs, health data and security events. Generally `Sensitive`; logging should avoid unnecessary payload or personal-data duplication.

### Secrets and credentials
API keys, passwords, bearer tokens, private keys and infrastructure credentials are `Restricted`. They must not be committed to source control, copied into tickets, screenshots or acceptance documents, or used as catalog evidence. IntelOwl API tokens and analyzer/provider credentials are included in this rule.

### Test and staging data
Prefer synthetic or sanitized representative data. Real production data requires explicit authorization, documented necessity and appropriate controls.

## TLP and external enrichment handling

DTMO classification and TLP/handling are related but distinct controls. External enrichment is permitted only where both classification/privacy and TLP/source restrictions allow disclosure.

- Unknown or missing handling state fails closed to review-required.
- `TLP:RED` or equivalently restricted data is not submitted to external analyzers.
- In the current governed execution slice, every requested IntelOwl analyzer is conservatively treated as an external disclosure target unless a future reviewed contract proves a narrower boundary.
- An IntelOwl analyzer's configured `maximum_tlp` is an additional guardrail, not a replacement for DTMO policy.
- A newly installed or discoverable analyzer is not automatically approved to receive DTMO data.
- Analyzer/playbook approval must record whether execution is internal or sends observable data to an external provider.
- External connector/share actions are not authorized merely because IntelOwl technically supports them.

## Retention principles

- retain data only while it supports an approved intelligence, security, audit, operational, legal or evidential purpose;
- preserve provenance and evidence integrity for as long as the corresponding intelligence/evidence must remain defensible;
- define deletion or archival behavior per data category and target environment;
- avoid indefinite retention by default;
- ensure backups and derived indexes follow the governing retention/deletion model where technically applicable;
- document exceptions where legal hold, incident response or external assurance requires extended retention;
- for external enrichment, retain only the result/provenance necessary for the approved CTI/security purpose and do not duplicate provider-side data unnecessarily.

## Logical retention model

| Data class | Baseline retention approach |
|---|---|
| Canonical intelligence | Policy-defined lifecycle based on intelligence relevance, source terms and organizational requirements |
| Raw evidence | Retain as needed to support provenance, auditability and accepted source/legal conditions |
| Enrichment results | Bounded policy-defined lifecycle tied to relevance, analyzer/provider terms and privacy requirements; retain source/job/analyzer attribution and remove corresponding derived/backed-up copies according to deployment policy |
| Search index | Rebuildable/supporting representation; lifecycle should follow canonical intelligence state |
| Audit records | Retain according to security/audit requirements and organizational policy |
| Operational metrics | Shorter operational lifecycle unless required for investigation or assurance |
| Secrets | Do not retain in DTMO documentation/evidence; lifecycle is controlled by secret-management system |
| CI artifacts | Retain according to evidence value and platform policy; immutable evidence needed for formal acceptance should be preserved appropriately |

This document intentionally does not invent fixed durations where the repository does not establish an authoritative legal/organizational requirement.

## Privacy and minimization

Personal data should be collected only where necessary for the defined CTI/security purpose. Logs and evidence packages should prefer identifiers, correlation references and bounded extracts over full sensitive payload replication.

Before enabling any IntelOwl analyzer for personal data, the accountable owner must document the data categories submitted, provider purpose and terms, processor/controller roles where applicable, transfer/location implications, retention, deletion and access controls. The current Phase 11.3 contract intentionally blocks email/generic personal-data enrichment pending that decision.

## Disposal

Deletion must consider canonical state, search/index copies, raw-object copies, caches, backups, retained enrichment results and exported evidence. Disposal of Restricted material must use the controls appropriate to the underlying secret/storage platform.

For IntelOwl durable history, deletion/archival implementation and backup propagation remain deployment-policy responsibilities to be validated in later industrialisation and production-equivalent phases; repository CI does not prove operational erasure or retention enforcement.

## Environment and lifecycle acceptance

Phase 8 and Phase 9 evidence remains historical and candidate-bound. Phase 10 denied production authorization. Because Phase 11 materially changes service composition and data flows, the integrated candidate requires fresh Phase 11.10 production-equivalent validation and Phase 11.11 independent assurance.

Production retention, external-enrichment policy, provider approvals and accountable ownership must be explicitly accepted before any future Phase 12 production `GO`. Repository contract/CI evidence does not establish that operational approval.
