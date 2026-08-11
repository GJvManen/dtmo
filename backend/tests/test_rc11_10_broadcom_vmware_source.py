from dtmo.broadcom_vmware_adapter import (
    BROADCOM_VMWARE_EXECUTION_PROFILE,
    discover_broadcom_vmware_advisories,
    parse_broadcom_vmware_advisory,
)
from dtmo.source_catalog import catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY
from dtmo.source_executor import SourceExecutionError


def test_broadcom_vmware_catalog_is_supported_and_registered() -> None:
    catalog = catalog_by_id("broadcom-vmware-advisories")
    assert catalog is not None
    assert catalog.endpoint_url == "https://www.broadcom.com/support/vmware-security-advisories"
    assert catalog.execution_profile == BROADCOM_VMWARE_EXECUTION_PROFILE
    assert catalog.execution_status == "supported"
    assert catalog.reliability == "authoritative"
    assert BROADCOM_VMWARE_EXECUTION_PROFILE in SOURCE_ADAPTER_REGISTRY.profiles()


def test_broadcom_vmware_discovery_is_first_party_bounded_and_deduplicated() -> None:
    payload = b"""<html><body>
      <a href='https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017'>VMSA-2026-0006: VMware updates</a>
      <a href='https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017'>VMSA-2026-0006 duplicate</a>
      <a href='https://evil.example/security/VMSA-2026-9999'>VMSA-2026-9999 untrusted</a>
    </body></html>"""
    discovered = discover_broadcom_vmware_advisories(
        payload,
        index_url="https://www.broadcom.com/support/vmware-security-advisories",
    )
    assert discovered == [
        (
            "VMSA-2026-0006",
            "https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017",
            "VMSA-2026-0006: VMware updates",
        )
    ]


def test_broadcom_vmware_parser_preserves_vmsa_and_cve_provenance() -> None:
    payload = b"""<html><body>
      <h1>VMSA-2026-0006: VMware ESX updates address multiple vulnerabilities</h1>
      <p>Affected CVE: CVE-2026-59309, CVE-2026-59310</p>
    </body></html>"""
    url = "https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017"
    record = parse_broadcom_vmware_advisory(
        payload,
        advisory_id="VMSA-2026-0006",
        url=url,
        discovery_title="VMSA-2026-0006: VMware ESX updates address multiple vulnerabilities",
        reliability="authoritative",
    )
    assert record.external_id == "VMSA-2026-0006"
    assert record.object_type == "security-advisory"
    assert record.url == url
    assert record.source_reliability == "authoritative"
    assert record.raw["advisory_id"] == "VMSA-2026-0006"
    assert record.raw["cves"] == ["CVE-2026-59309", "CVE-2026-59310"]


def test_broadcom_vmware_parser_fails_closed_without_matching_id_or_cves() -> None:
    url = "https://support.broadcom.com/web/ecx/support-content-notification/-/external/content/SecurityAdvisories/0/38017"
    try:
        parse_broadcom_vmware_advisory(
            b"<html><body>VMSA-2026-0005 CVE-2026-59309</body></html>",
            advisory_id="VMSA-2026-0006",
            url=url,
            discovery_title="VMSA-2026-0006",
            reliability="authoritative",
        )
    except SourceExecutionError as exc:
        assert "identifier mismatch" in str(exc)
    else:
        raise AssertionError("mismatched VMSA identifier must fail closed")

    try:
        parse_broadcom_vmware_advisory(
            b"<html><body>VMSA-2026-0006 no CVE identifiers</body></html>",
            advisory_id="VMSA-2026-0006",
            url=url,
            discovery_title="VMSA-2026-0006",
            reliability="authoritative",
        )
    except SourceExecutionError as exc:
        assert "no published CVE" in str(exc)
    else:
        raise AssertionError("VMSA without CVE identifiers must fail closed")
