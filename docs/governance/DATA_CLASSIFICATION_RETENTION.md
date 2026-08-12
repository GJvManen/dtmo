# DTMO Data Classification and Retention Model

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

### Identity and authorization data
Principal identifiers, roles, assignments and audit-relevant authorization state. Generally `Sensitive`.

### Audit and operational telemetry
Actor/action context, correlation IDs, health data and security events. Generally `Sensitive`; logging should avoid unnecessary payload or personal-data duplication.

### Secrets and credentials
API keys, passwords, bearer tokens, private keys and infrastructure credentials are `Restricted`. They must not be committed to source control, copied into tickets, screenshots or acceptance documents, or used as catalog evidence.

### Test and staging data
Prefer synthetic or sanitized representative data. Real production data requires explicit authorization, documented necessity and appropriate controls.

## Retention principles

- retain data only while it supports an approved intelligence, security, audit, operational, legal or evidential purpose;
- preserve provenance and evidence integrity for as long as the corresponding intelligence/evidence must remain defensible;
- define deletion or archival behavior per data category and target environment;
- avoid indefinite retention by default;
- ensure backups and derived indexes follow the governing retention/deletion model where technically applicable;
- document exceptions where legal hold, incident response or external assurance requires extended retention.

## Logical retention model

| Data class | Baseline retention approach |
|---|---|
| Canonical intelligence | Policy-defined lifecycle based on intelligence relevance, source terms and organizational requirements |
| Raw evidence | Retain as needed to support provenance, auditability and accepted source/legal conditions |
| Search index | Rebuildable/supporting representation; lifecycle should follow canonical intelligence state |
| Audit records | Retain according to security/audit requirements and organizational policy |
| Operational metrics | Shorter operational lifecycle unless required for investigation or assurance |
| Secrets | Do not retain in DTMO documentation/evidence; lifecycle is controlled by secret-management system |
| CI artifacts | Retain according to evidence value and platform policy; immutable evidence needed for formal acceptance should be preserved appropriately |

This document intentionally does not invent fixed durations where the repository does not establish an authoritative legal/organizational requirement.

## Privacy and minimization

Personal data should be collected only where necessary for the defined CTI/security purpose. Logs and evidence packages should prefer identifiers, correlation references and bounded extracts over full sensitive payload replication.

## Disposal

Deletion must consider canonical state, search/index copies, raw-object copies, caches, backups and exported evidence. Disposal of Restricted material must use the controls appropriate to the underlying secret/storage platform.

## Environment acceptance

Phase 8 must record the staging data-class and sanitization approach and confirm that production credentials are not used. Production retention configuration and ownership must be explicitly accepted before Phase 10 go/no-go.
