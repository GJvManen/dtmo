from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class CatalogSource:
    id: str
    name: str
    endpoint_url: str
    reliability: str
    category: str
    execution_profile: str
    execution_status: str
    provenance_note: str
    recommended_interval_seconds: int = 3600
    secret_ref: str | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


# Curated, code-reviewed source inventory. Catalog membership is not publication
# approval and does not by itself enable execution. `supported` entries have an
# accepted parser. Other entries remain visible for governed onboarding work.
SOURCE_CATALOG: tuple[CatalogSource, ...] = (
    CatalogSource(id="cisa-kev", name="CISA Known Exploited Vulnerabilities", endpoint_url="https://www.cisa.gov/known-exploited-vulnerabilities-catalog", reliability="authoritative", category="exploited-vulnerabilities", execution_profile="built-in-cisa-kev", execution_status="supported-built-in", provenance_note="CISA authoritative catalog of vulnerabilities known to be exploited in the wild.", recommended_interval_seconds=3600),
    CatalogSource(id="nvd-cve", name="NIST National Vulnerability Database CVE API 2.0", endpoint_url="https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=100", reliability="authoritative", category="vulnerabilities", execution_profile="nvd-cve-v2", execution_status="supported", provenance_note="NIST NVD CVE API 2.0; CVE records with NVD enrichment and source attribution.", recommended_interval_seconds=7200),
    CatalogSource(id="github-global-advisories", name="GitHub Global Security Advisories", endpoint_url="https://api.github.com/advisories?per_page=100", reliability="high", category="software-supply-chain", execution_profile="github-global-advisories-v1", execution_status="supported", provenance_note="GitHub-reviewed global security advisories; public advisory resources can be queried without authentication.", recommended_interval_seconds=3600),
    CatalogSource(id="ncsc-nl-advisories", name="NCSC-NL Security Advisories (CSAF)", endpoint_url="https://advisories.ncsc.nl/csaf/", reliability="authoritative", category="nl-security-advisories", execution_profile="csaf-2.0", execution_status="supported", provenance_note="Dutch NCSC machine-readable Security Advisories via the official CSAF provider distribution and v2 index.", recommended_interval_seconds=1800),
    CatalogSource(id="ncsc-nl-advisories-rss", name="NCSC-NL Security Advisories RSS", endpoint_url="https://advisories.ncsc.nl/rss/advisories", reliability="authoritative", category="nl-security-advisories", execution_profile="rss-2.0", execution_status="supported", provenance_note="Official NCSC-NL RSS distribution channel for Security Advisories.", recommended_interval_seconds=1800),
    CatalogSource(id="cert-eu-advisories", name="CERT-EU Security Advisories", endpoint_url="https://cert.europa.eu/publications/security-advisories/2026", reliability="authoritative", category="eu-security-advisories", execution_profile="cert-eu-advisories-v1", execution_status="supported", provenance_note="CERT-EU public advisory year index with official per-advisory JSON documents.", recommended_interval_seconds=3600),
    CatalogSource(id="msrc-security-update-guide", name="Microsoft Security Response Center Security Update Guide", endpoint_url="https://api.msrc.microsoft.com/cvrf/v3.0", reliability="authoritative", category="vendor-advisories", execution_profile="msrc-cvrf-v3", execution_status="supported", provenance_note="Official public MSRC CVRF v3 API: update summaries plus detailed CVRF security-update documents.", recommended_interval_seconds=3600),
    CatalogSource(id="cisco-security-advisories", name="Cisco Security Advisories", endpoint_url="https://apix.cisco.com/security/advisories/v2", reliability="authoritative", category="vendor-advisories", execution_profile="cisco-openvuln-v2", execution_status="supported", provenance_note="Official Cisco PSIRT OpenVuln API v2. Runtime execution requires a bearer credential referenced outside source control.", recommended_interval_seconds=3600, secret_ref="env:CISCO_OPENVULN_TOKEN"),
    CatalogSource(id="redhat-security", name="Red Hat Product Security", endpoint_url="https://access.redhat.com/security/security-updates/", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-redhat", execution_status="planned-parser", provenance_note="Official Red Hat product security and security-update information."),
    CatalogSource(id="ubuntu-security-notices", name="Ubuntu Security Notices", endpoint_url="https://ubuntu.com/security/notices", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-ubuntu", execution_status="planned-parser", provenance_note="Official Canonical Ubuntu Security Notices."),
    CatalogSource(id="debian-security", name="Debian Security Information", endpoint_url="https://www.debian.org/security/", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-debian", execution_status="planned-parser", provenance_note="Official Debian security advisory surface."),
    CatalogSource(id="apple-security-releases", name="Apple Security Releases", endpoint_url="https://support.apple.com/100100", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-apple", execution_status="planned-parser", provenance_note="Official Apple security releases and security-content references."),
    CatalogSource(id="google-chrome-releases", name="Chrome Releases", endpoint_url="https://chromereleases.googleblog.com/", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-chrome", execution_status="planned-parser", provenance_note="Official Google Chrome release and security-fix publication surface."),
    CatalogSource(id="mozilla-security-advisories", name="Mozilla Foundation Security Advisories", endpoint_url="https://www.mozilla.org/security/advisories/", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-mozilla", execution_status="planned-parser", provenance_note="Official Mozilla security advisories."),
    CatalogSource(id="fortinet-psirt", name="Fortinet PSIRT Advisories", endpoint_url="https://www.fortiguard.com/psirt", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-fortinet", execution_status="planned-parser", provenance_note="Official Fortinet PSIRT advisory surface."),
    CatalogSource(id="paloalto-security-advisories", name="Palo Alto Networks Security Advisories", endpoint_url="https://security.paloaltonetworks.com/", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-paloalto", execution_status="planned-parser", provenance_note="Official Palo Alto Networks product security advisory surface."),
    CatalogSource(id="broadcom-vmware-advisories", name="Broadcom VMware Security Advisories", endpoint_url="https://support.broadcom.com/web/ecx/security-advisory", reliability="authoritative", category="vendor-advisories", execution_profile="vendor-broadcom-vmware", execution_status="planned-parser", provenance_note="Official Broadcom/VMware security-advisory surface."),
    CatalogSource(id="enisa-threat-landscape", name="ENISA Threat Landscape", endpoint_url="https://www.enisa.europa.eu/topics/cyber-threats/threats-and-trends", reliability="authoritative", category="strategic-threat-intelligence", execution_profile="research-publication", execution_status="research-reference", provenance_note="ENISA strategic threat-landscape and trends publications; not a high-frequency vulnerability feed.", recommended_interval_seconds=86400),
)


def catalog_by_id(source_id: str) -> CatalogSource | None:
    return next((item for item in SOURCE_CATALOG if item.id == source_id), None)
