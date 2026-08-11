# DTMO source connection matrix

Status: maintained release contract

A catalog entry is **connected** only when its execution status is `supported` or `supported-built-in`, its execution profile has an accepted executor, it can be reached through the unified console/bootstrap flow (or the explicit built-in path), and regression tests preserve provenance and fail-closed behaviour.

| Source | Profile | Status | Execution path |
|---|---|---|---|
| CISA KEV | `built-in-cisa-kev` | CONNECTED | Built-in CISA KEV connector/run path |
| NIST NVD CVE API 2.0 | `nvd-cve-v2` | CONNECTED | Registry bootstrap -> enable -> run |
| GitHub Global Security Advisories | `github-global-advisories-v1` | CONNECTED | Registry bootstrap -> enable -> run |
| NCSC-NL Security Advisories CSAF | `csaf-2.0` | CONNECTED | Registry bootstrap -> enable -> official CSAF v2 index/documents |
| NCSC-NL Security Advisories RSS | `rss-2.0` | CONNECTED | Registry bootstrap -> enable -> run |
| CERT-EU Security Advisories | `cert-eu-advisories-v1` | CONNECTED | Registry bootstrap -> enable -> official year index + per-advisory JSON |
| Microsoft Security Response Center | `msrc-cvrf-v3` | PENDING_CI | Registry bootstrap -> enable -> official MSRC `/updates` + `/cvrf/{id}` API |
| Cisco Security Advisories | `vendor-cisco` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Red Hat Product Security | `vendor-redhat` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Ubuntu Security Notices | `vendor-ubuntu` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Debian Security Information | `vendor-debian` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Apple Security Releases | `vendor-apple` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Chrome Releases | `vendor-chrome` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Mozilla Security Advisories | `vendor-mozilla` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Fortinet PSIRT | `vendor-fortinet` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Palo Alto Networks Security Advisories | `vendor-paloalto` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| Broadcom/VMware Security Advisories | `vendor-broadcom-vmware` | ADAPTER_REQUIRED | Visible in catalog; execution disabled |
| ENISA Threat Landscape | `research-publication` | RESEARCH_REFERENCE | Deliberately not a high-frequency ingestion feed |

## Enforced contract

`backend/tests/test_rc9_safe_source_execution.py` requires the set of all `supported` catalog execution profiles to match `SUPPORTED_REGISTRY_EXECUTION_PROFILES` in `dtmo.source_executor`. A source therefore cannot be promoted to `supported` without an explicit governed executor. `supported-built-in` is separately constrained to the CISA KEV built-in path.

## Remaining onboarding order

After MSRC acceptance, remaining operational vendor sources are onboarded one by one against official machine-readable APIs/feeds where available. A vendor source stays fail-closed as `planned-parser` until its endpoint contract, bounded fetch behaviour, normalization, provenance, tests and exact-head release gates are accepted.
