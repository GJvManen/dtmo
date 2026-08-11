from dtmo.mozilla_adapter import (
    MOZILLA_EXECUTION_PROFILE,
    discover_mozilla_advisories,
    parse_mozilla_advisory,
)
from dtmo.source_catalog import catalog_by_id
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY


def test_mozilla_catalog_and_registry_contract() -> None:
    source = catalog_by_id("mozilla-security-advisories")
    assert source is not None
    assert source.execution_status == "supported"
    assert source.execution_profile == MOZILLA_EXECUTION_PROFILE
    assert source.endpoint_url == "https://www.mozilla.org/security/advisories/"
    assert MOZILLA_EXECUTION_PROFILE in SOURCE_ADAPTER_REGISTRY.profiles()


def test_discover_mozilla_advisories_is_first_party_bounded_and_deduplicated() -> None:
    payload = b'''<html><body>
    <a href="/en-US/security/advisories/mfsa2026-69/">Firefox ESR advisory</a>
    <a href="https://www.mozilla.org/en-US/security/advisories/mfsa2026-67/">Firefox advisory</a>
    <a href="https://evil.example/security/advisories/mfsa2026-66/">bad</a>
    <a href="/en-US/security/advisories/mfsa2026-69/">duplicate</a>
    </body></html>'''
    items = discover_mozilla_advisories(payload)
    assert [item[0] for item in items] == ["mfsa2026-69", "mfsa2026-67"]
    assert all(item[1].startswith("https://www.mozilla.org/security/advisories/") for item in items)


def test_parse_mozilla_advisory_preserves_cves_and_provenance() -> None:
    payload = b'''<html><body><h1>Mozilla Foundation Security Advisory 2026-69</h1>
    <h2>Security Vulnerabilities fixed in Firefox ESR 115.38</h2>
    <p>CVE-2026-15719</p><p>CVE-2026-16349</p></body></html>'''
    record = parse_mozilla_advisory(
        payload,
        advisory_id="mfsa2026-69",
        url="https://www.mozilla.org/security/advisories/mfsa2026-69/",
        title="Security Vulnerabilities fixed in Firefox ESR 115.38",
        reliability="authoritative",
    )
    assert record.external_id == "MFSA2026-69"
    assert record.raw["cves"] == ["CVE-2026-15719", "CVE-2026-16349"]
    assert record.source_reliability == "authoritative"
