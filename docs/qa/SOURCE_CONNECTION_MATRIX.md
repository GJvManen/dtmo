# DTMO source connection matrix

Status: maintained release contract

A catalog entry is **connected** only when its execution status is `supported` or `supported-built-in`, its execution profile has an accepted adapter in the unified source framework, it can be reached through the unified console/bootstrap flow (or the explicit built-in path), and regression tests preserve provenance and fail-closed behaviour.

| Source | Profile | Status | Execution path |
|---|---|---|---|
| CISA KEV | `built-in-cisa-kev` | CONNECTED | Built-in CISA KEV connector/run path |
| NIST NVD CVE API 2.0 | `nvd-cve-v2` | CONNECTED | Registry bootstrap -> enable -> run |
| GitHub Global Security Advisories | `github-global-advisories-v1` | CONNECTED | Registry bootstrap -> enable -> run |
| NCSC-NL Security Advisories CSAF | `csaf-2.0` | CONNECTED | Registry bootstrap -> enable -> official CSAF v2 index/documents |
| NCSC-NL Security Advisories RSS | `rss-2.0` | CONNECTED | Registry bootstrap -> enable -> run |
| CERT-EU Security Advisories | `cert-eu-advisories-v1` | CONNECTED | Registry bootstrap -> enable -> official year index + per-advisory JSON |
| Microsoft Security Response Center | `msrc-cvrf-v3` | CONNECTED | Registry bootstrap -> enable -> official MSRC `/updates` + `/cvrf/{id}` API |
| Cisco Security Advisories | `cisco-openvuln-v2` | CONNECTED | Registry bootstrap -> inject `env:CISCO_OPENVULN_TOKEN` -> enable -> official Cisco PSIRT OpenVuln `/latest/25` |
| Red Hat Product Security | `redhat-csaf-v1` | CONNECTED | Registry bootstrap -> enable -> official Red Hat Security Data API `/csaf.json` + `/csaf/{RHSA}.json` |
| Ubuntu Security Notices | `rss-2.0` | CONNECTED | Registry bootstrap -> enable -> official Canonical `/security/notices/rss.xml` feed |
| Debian Security Advisories | `rss-2.0` | CONNECTED | Registry bootstrap -> enable -> official Debian `/security/dsa` RSS feed |
| Apple Security Releases | `apple-security-releases-v1` | CONNECTED | Registry bootstrap -> enable -> bounded first-party Apple Support `100100` security-release index |
| Chrome Releases | `chrome-security-releases-v1` | CONNECTED | Registry bootstrap -> enable -> bounded first-party Chrome Releases stable posts -> published CVE validation |
| Mozilla Security Advisories | `mozilla-mfsa-v1` | CONNECTED | Registry bootstrap -> enable -> bounded first-party Mozilla MFSA index/detail documents -> published CVE validation |
| Fortinet PSIRT | `fortinet-psirt-v1` | PENDING_CI | Registry bootstrap -> enable -> bounded FortiGuard PSIRT FG-IR index/detail documents -> published CVE validation |
| Palo Alto Networks Security Advisories | `vendor-paloalto` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Broadcom/VMware Security Advisories | `vendor-broadcom-vmware` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| ENISA Threat Landscape | `research-publication` | RESEARCH_REFERENCE | Deliberately not a high-frequency ingestion feed |

## Enforced contract

`backend/tests/test_rc11_1_source_framework.py` requires every `supported` catalog execution profile to exist in the unified `SourceAdapterRegistry`. Ubuntu and Debian reuse the accepted `rss-2.0` adapter. Apple, Chrome, Mozilla and Fortinet use dedicated bounded first-party publication adapters where a documented list API is not accepted as the integration contract. `supported-built-in` remains separately constrained to the CISA KEV built-in path.

Credential values are never stored in the catalog or source registry. Credentialed catalog entries carry only a logical secret reference such as `env:CISCO_OPENVULN_TOKEN`; execution fails closed when the referenced runtime secret is absent or the reference scheme is not accepted.

## Remaining onboarding order

After Fortinet acceptance, Palo Alto Networks and Broadcom/VMware remain. Each source stays fail-closed as `planned-parser` until its official endpoint contract, bounded fetch behaviour, normalization, provenance, tests and exact-head release gates are accepted.
