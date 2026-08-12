# DTMO Intelligence Source Catalog

Last reviewed: **2026-08-12**  
Baseline: **16.0.0rc12 / RC13 accepted**

## Purpose

DTMO separates source cataloguing, registration, enablement, execution, candidate ingestion, human review and external-share approval.

Catalog membership or technical source execution never grants publication authority.

## Source classes

### Built-in source

| Source | Reliability | Execution model | Status |
|---|---|---|---|
| CISA Known Exploited Vulnerabilities (KEV) | authoritative | built-in connector | supported built-in |

### Supported executable catalog sources

The current code-reviewed source catalog includes the following executable profiles:

| Source | Category | Execution profile | Reliability | Credential requirement |
|---|---|---|---|---|
| NIST NVD CVE API 2.0 | vulnerabilities | `nvd-cve-v2` | authoritative | none for bounded public use |
| GitHub Global Security Advisories | software supply chain | `github-global-advisories-v1` | high | public endpoint for current profile |
| NCSC-NL Security Advisories (CSAF) | NL security advisories | `csaf-2.0` | authoritative | none |
| NCSC-NL Security Advisories RSS | NL security advisories | `rss-2.0` | authoritative | none |
| CERT-EU Security Advisories | EU security advisories | `cert-eu-advisories-v1` | authoritative | none |
| Microsoft Security Response Center | vendor advisories | `msrc-cvrf-v3` | authoritative | none for current public profile |
| Cisco Security Advisories | vendor advisories | `cisco-openvuln-v2` | authoritative | logical reference `env:CISCO_OPENVULN_TOKEN` |
| Red Hat Product Security | vendor advisories | `redhat-csaf-v1` | authoritative | none |
| Ubuntu Security Notices | vendor advisories | `rss-2.0` | authoritative | none |
| Debian Security Advisories | vendor advisories | `rss-2.0` | authoritative | none |
| Apple Security Releases | vendor advisories | `apple-security-releases-v1` | authoritative | none |
| Chrome Releases | vendor advisories | `chrome-security-releases-v1` | authoritative | none |
| Mozilla Foundation Security Advisories | vendor advisories | `mozilla-mfsa-v1` | authoritative | none |
| Fortinet PSIRT Advisories | vendor advisories | `fortinet-psirt-v1` | authoritative | none |
| Palo Alto Networks Security Advisories | vendor advisories | `rss-2.0` | authoritative | none |
| Broadcom/VMware Security Advisories | vendor advisories | `broadcom-vmware-vmsa-v1` | authoritative | none |

### Strategic/research reference

| Source | Use | Execution status |
|---|---|---|
| ENISA Threat Landscape | strategic threat landscape and trends | research reference, not high-frequency executable vulnerability feed |

## Education-sector enrichment targets

Education-specific sources remain important enrichment/onboarding targets where access terms and machine interfaces permit automation, including:

- School-CERT / Kennisnet sector alerts and threat analyses;
- School-CERT primary/secondary education threat picture;
- SURF cyber threat picture for education and research;
- SURFcert / Security Expertise Centre operational context.

Participant-only/member-only content must not be automated unless an approved interface and lawful distribution basis are established.

## Catalog bootstrap behavior

Code-reviewed executable catalog entries can be registered into the governed source registry through the catalog bootstrap flow.

Security behavior:

- registered catalog sources default to **disabled**;
- bootstrap is idempotent;
- a human administrator with connector-management authority controls registration/enablement;
- credentialed sources store only logical secret references;
- source lifecycle mutations are audited;
- technical source execution does not alter review/share authority.

The built-in CISA KEV connector remains a built-in execution path and is represented distinctly from executable registry catalog entries.

## Manual source registration — current capability and UX gap

The backend already provides governed manual source-registry APIs, including:

- create source;
- update source;
- list source definitions;
- validate source;
- enable/disable state;
- reliability/interval configuration;
- logical `secret_ref` support;
- human-admin/RBAC enforcement;
- persistent audit events with request correlation.

Current registry source types are constrained to the supported registry contract (`cisa-kev` / `json-feed`) and source URLs are validated as public HTTPS endpoints.

**Current product gap:** the accepted owner-facing `Sources & Catalog` interface does not yet expose a complete professional manual-source onboarding workflow. Post-RC13 enhancement E2 should therefore build the governed canonical UI journey on top of the existing backend capabilities and extend contracts only where needed, rather than introducing a parallel source registry.

## Source URL and SSRF protection

Generic registry/source execution applies a fail-closed network contract. Relevant controls include:

- HTTPS-only registered source URLs;
- no embedded credentials;
- default HTTPS port;
- rejection of local/internal/non-global literal destinations;
- runtime address validation to mitigate DNS rebinding;
- redirect restrictions where required by the execution profile;
- controlled content type/response size;
- bounded parsing/normalization through known execution profiles.

## Normalization and canonical persistence

Supported source records enter the governed intelligence pipeline:

```text
source fetch
  -> raw evidence retention
  -> profile-specific normalization/provenance
  -> canonical PostgreSQL persistence
  -> OpenSearch search/index representation
  -> Intelligence / Overview / Visual Analytics
```

Canonical normalization preserves the HTTP(S)-only canonical reference boundary and known intelligence types. Explicit supported aliases may be normalized; unknown types fail closed.

For NVD CVEs, a stable NVD HTTPS detail page is used for canonical/provenance identity while upstream references—including non-HTTP references—remain in raw evidence.

Canonical application success requires the PostgreSQL transaction to commit before a connector run is treated as durably successful.

## New source acceptance requirements

Any new adapter/profile or expanded manual source type requires, as applicable:

- explicit source ownership and access/legal basis;
- endpoint/profile contract;
- provenance mapping;
- fixture-based parser/normalization tests;
- safe runtime egress/SSRF controls;
- credential/secret-reference contract;
- timeout/retry/freshness/failure-isolation behavior;
- raw evidence and canonical persistence behavior;
- replay/idempotency expectations;
- audit/RBAC controls;
- licensing/terms/distribution notes;
- exact-head release evidence.

## Planned source UX enhancement

The next dedicated Sources & Catalog enhancement should provide an operator-friendly manual onboarding flow for:

1. source ID/name/type;
2. endpoint;
3. reliability;
4. interval/freshness expectation;
5. authentication mode and logical secret reference;
6. owner/context;
7. validation/test-run;
8. default-disabled registration;
9. explicit activation;
10. audit/result feedback.

It must reuse the canonical registry and preserve least privilege, auditability and publication-authority separation.
