# DTMO Source Connection Matrix

Last reviewed: **2026-08-12**  
Status: **maintained release contract for the accepted RC13 baseline**

## Connection definition

A catalog entry is `CONNECTED` only when:

- its catalog execution state is supported/supported-built-in;
- its execution profile is implemented in the accepted source framework or explicit built-in path;
- it can be registered/bootstraped where applicable;
- it can be enabled and executed through governed source operations;
- normalization/provenance behavior is covered by regression evidence;
- unsupported/invalid input fails closed.

`CONNECTED` is a software integration claim, not a provider-SLA, production-credential, legal-distribution or staging-acceptance claim.

## Current source matrix

| Source | Profile | Status | Governed execution path |
|---|---|---|---|
| CISA KEV | `built-in-cisa-kev` | `CONNECTED` | Explicit built-in CISA KEV run path |
| NIST NVD CVE API 2.0 | `nvd-cve-v2` | `CONNECTED` | Catalog registration → enable → run |
| GitHub Global Security Advisories | `github-global-advisories-v1` | `CONNECTED` | Catalog registration → enable → run |
| NCSC-NL Security Advisories CSAF | `csaf-2.0` | `CONNECTED` | Catalog registration → enable → official CSAF distribution |
| NCSC-NL Security Advisories RSS | `rss-2.0` | `CONNECTED` | Catalog registration → enable → run |
| CERT-EU Security Advisories | `cert-eu-advisories-v1` | `CONNECTED` | Catalog registration → enable → official advisory documents |
| Microsoft Security Response Center | `msrc-cvrf-v3` | `CONNECTED` | Catalog registration → enable → official MSRC API |
| Cisco Security Advisories | `cisco-openvuln-v2` | `CONNECTED` | Catalog registration → logical token reference → enable → Cisco API |
| Red Hat Product Security | `redhat-csaf-v1` | `CONNECTED` | Catalog registration → enable → official security-data/CSAF API |
| Ubuntu Security Notices | `rss-2.0` | `CONNECTED` | Catalog registration → enable → official RSS |
| Debian Security Advisories | `rss-2.0` | `CONNECTED` | Catalog registration → enable → official RSS |
| Apple Security Releases | `apple-security-releases-v1` | `CONNECTED` | Catalog registration → enable → bounded first-party discovery |
| Chrome Releases | `chrome-security-releases-v1` | `CONNECTED` | Catalog registration → enable → bounded first-party stable-release discovery |
| Mozilla Security Advisories | `mozilla-mfsa-v1` | `CONNECTED` | Catalog registration → enable → bounded first-party MFSA discovery |
| Fortinet PSIRT | `fortinet-psirt-v1` | `CONNECTED` | Catalog registration → enable → bounded FortiGuard PSIRT discovery |
| Palo Alto Networks Security Advisories | `rss-2.0` | `CONNECTED` | Catalog registration → enable → official RSS |
| Broadcom/VMware Security Advisories | `broadcom-vmware-vmsa-v1` | `CONNECTED` | Catalog registration → enable → bounded first-party VMSA discovery |
| ENISA Threat Landscape | `research-publication` | `RESEARCH_REFERENCE` | Strategic/context source; deliberately not a high-frequency executable feed |

## Shared adapter and execution contracts

Where providers expose compatible formats, DTMO reuses governed shared profiles instead of duplicating parser implementations. Dedicated adapters are used where provider discovery/document formats require bounded first-party handling.

The source framework must preserve:

- provider/source identity;
- safe endpoint/network behavior;
- profile-specific parsing;
- canonical intelligence type/reference normalization;
- provenance and raw evidence;
- timeout/retry/freshness/failure isolation;
- idempotent/replay behavior where defined;
- canonical commit-before-success behavior.

## Credentialed sources

Credential values are never stored in the source catalog or registry. Credentialed entries use logical secret references (for example `env:CISCO_OPENVULN_TOKEN`) and fail closed when a required runtime secret cannot be resolved.

Staging/production secret references must map to approved least-privilege identities and must not reuse local-development infrastructure/root credential exceptions.

## Canonical persistence contract

A successful source run progresses through:

```text
provider fetch
  -> raw evidence
  -> canonical normalization/provenance
  -> PostgreSQL durable commit
  -> OpenSearch index/search representation
  -> Intelligence / Overview / Visual Analytics
```

PostgreSQL is the canonical application state. A raw-object write or OpenSearch `201` by itself is not equivalent to durable canonical intelligence acceptance.

## Normalization contract

The accepted baseline includes fail-closed normalization for supported source records. Examples:

- NVD uses a stable HTTPS NVD CVE detail page for canonical/provenance identity while retaining upstream references in raw evidence;
- the explicit supported `security-advisory` alias is normalized to canonical `advisory`;
- unknown intelligence types remain fail closed;
- canonical URL requirements remain HTTP(S)-only where defined by the intelligence schema.

## Canonical console operations

The unified `Sources & Catalog` area is the intended operator-facing source workspace. It exposes catalog/registry state and governed execution controls without granting review/share authority.

The backend already supports manual source create/update/list/validate operations under human-admin/RBAC control. The current owner-facing product gap is the absence of a complete professional **manual source onboarding UI journey**. That UI enhancement is tracked after the shared severity/filter enhancement.

## Education-sector/context sources

School-CERT/Kennisnet and SURF/SURFcert material can provide valuable education-specific threat context. Member/participant-only content must only be automated when an approved interface and legal/distribution basis exist.

## Claim boundary

`CONNECTED` does not itself establish:

- current provider availability/SLA;
- possession/approval of production credentials;
- lawful redistribution rights beyond the relevant source terms;
- production-equivalent staging acceptance;
- external-share/publication authority.

Those remain separate operational, legal/governance and production-readiness evidence classes.
