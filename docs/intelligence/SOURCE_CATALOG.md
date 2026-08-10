# DTMO curated intelligence source catalog

Last reviewed: 2026-08-10

DTMO separates cataloguing, registration, execution, candidate ingestion, human review and external share approval. Catalog membership never grants trust or publication authority.

## Directly supported in 16.0.0rc9

- CISA Known Exploited Vulnerabilities — authoritative, built-in connector.
- NIST NVD CVE API 2.0 — authoritative, `nvd-cve-v2` parser through the safe JSON executor.
- GitHub Global Security Advisories — high reliability, `github-global-advisories-v1` parser through the safe JSON executor.
- DTMO JSON v1 — governed custom JSON feeds using the documented canonical `items[]` contract.

Supported catalog entries are bootstrapped disabled. A human admin must explicitly enable a registered source before it can be executed.

## Curated onboarding backlog

The code-reviewed catalog additionally tracks NCSC-NL Security Advisories (CSAF and RSS), CERT-EU Security Advisories, Microsoft MSRC Security Update Guide, Cisco Security Advisories, Red Hat Product Security, Ubuntu Security Notices, Debian Security, Apple Security Releases, Chrome Releases, Mozilla Foundation Security Advisories, Fortinet PSIRT, Palo Alto Networks Security Advisories, Broadcom/VMware Security Advisories and ENISA Threat Landscape.

Education-specific research and partner sources are also retained as onboarding targets: School-CERT/Kennisnet sector alerts and threat analyses, the School-CERT primary/secondary education threat picture, SURF's cyber threat picture for education and research, and SURFcert/Security Expertise Centre operational context. Participant-only or member-only material must only be automated when an approved interface and distribution basis exist.

## Education-sector context

Public School-CERT material reports that Dutch schools manage sensitive employee, pupil and parent information and documents incidents affecting teaching continuity, exams, procurement, credentials and ICT resources. Its 2025 threat picture identifies recurring education risks. SURF's 2025 education-and-research threat picture highlights DDoS, malware and phishing and also discusses AI-enabled attacks, quantum preparation and digital-sovereignty dependencies. These publications are context/provenance sources rather than automatic publication feeds.

## Safe generic execution contract

For every generic JSON source run, DTMO re-validates the HTTPS URL, resolves DNS immediately before connection, rejects the complete answer set if any destination is non-global, connects to a validated IP while preserving the original hostname for TLS SNI/certificate validation, rejects redirects, avoids environment proxy configuration, accepts only JSON and caps responses at 5 MiB. Only known profiles or the DTMO JSON v1 contract are normalized.

Normalized records enter the existing raw-object, canonical database, provenance and OpenSearch pipeline. Connector health/failure isolation and alerting remain active, while repeated ingestion stays idempotent and can repair derived search state. Source execution never changes review or share-approval authority.

## Priority order for additional adapters

1. NCSC-NL CSAF.
2. Approved School-CERT/SURF machine interfaces where access terms permit automation.
3. CERT-EU advisory JSON discovery.
4. Microsoft and major infrastructure/security vendor advisories.
5. Strategic/research enrichment such as ENISA threat-landscape material.

Every new adapter requires provenance mapping, fixture-based parser tests, runtime egress tests, replay/health evidence, and explicit access/licensing notes before being marked executable.
