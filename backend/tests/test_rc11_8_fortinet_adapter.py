from dtmo.fortinet_adapter import (
    FORTINET_EXECUTION_PROFILE,
    _canonical_fortinet_advisory_url,
    discover_fortinet_advisories,
    parse_fortinet_advisory,
)
from dtmo.source_catalog import catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY


def test_fortinet_catalog_is_supported_and_registered() -> None:
    entry = catalog_by_id("fortinet-psirt")
    assert entry is not None
    assert entry.execution_status == "supported"
    assert entry.execution_profile == FORTINET_EXECUTION_PROFILE
    assert SOURCE_ADAPTER_REGISTRY.get(FORTINET_EXECUTION_PROFILE) is not None


def test_fortinet_url_filter_is_first_party_and_strict() -> None:
    assert _canonical_fortinet_advisory_url("/psirt/FG-IR-26-098") == (
        "FG-IR-26-098",
        "https://www.fortiguard.com/psirt/FG-IR-26-098",
    )
    assert _canonical_fortinet_advisory_url("https://evil.example/psirt/FG-IR-26-098") is None
    assert _canonical_fortinet_advisory_url("/threat-signal/FG-IR-26-098") is None


def test_fortinet_discovery_deduplicates_and_bounds() -> None:
    links = "".join(
        f'<a href="/psirt/FG-IR-26-{index:03d}">Issue {index}</a>' for index in range(30)
    )
    links += '<a href="/psirt/FG-IR-26-001">duplicate</a>'
    discovered = discover_fortinet_advisories(links.encode())
    assert len(discovered) == 25
    assert len({item[0] for item in discovered}) == 25


def test_fortinet_detail_requires_matching_id_and_cve_and_keeps_provenance() -> None:
    record = parse_fortinet_advisory(
        b"<html>FG-IR-26-098 Buffer overflow CVE-2025-54820 Download CVRF CSAF</html>",
        advisory_id="FG-IR-26-098",
        url="https://www.fortiguard.com/psirt/FG-IR-26-098",
        discovery_title="Buffer overflow via fgtupdates service",
        reliability="authoritative",
    )
    assert record.external_id == "FG-IR-26-098"
    assert record.raw["cves"] == ["CVE-2025-54820"]
    assert record.raw["url"].startswith("https://www.fortiguard.com/psirt/")
