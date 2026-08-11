import pytest

from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import SourceExecutionError, parse_registered_source
from dtmo.source_framework import SOURCE_ADAPTER_REGISTRY
from dtmo.sources import SourceDefinition


def _source() -> SourceDefinition:
    return SourceDefinition(
        id="paloalto-security-advisories",
        name="Palo Alto Networks Security Advisories",
        source_type="json-feed",
        endpoint_url="https://security.paloaltonetworks.com/rss.xml",
        enabled=True,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="test",
        updated_by="test",
    )


def test_paloalto_catalog_uses_official_supported_rss() -> None:
    catalog = catalog_by_id("paloalto-security-advisories")
    assert catalog is not None
    assert catalog.endpoint_url == "https://security.paloaltonetworks.com/rss.xml"
    assert catalog.execution_profile == "rss-2.0"
    assert catalog.execution_status == "supported"
    assert catalog.reliability == "authoritative"
    assert "rss-2.0" in SOURCE_ADAPTER_REGISTRY.profiles()


def test_paloalto_rss_normalizes_advisory_and_preserves_provenance() -> None:
    payload = b"""<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'>
      <channel>
        <title>Palo Alto Networks Security Advisories</title>
        <item>
          <title>CVE-2026-0288 PAN-OS: Buffer Overflow Vulnerabilities</title>
          <link>https://security.paloaltonetworks.com/CVE-2026-0288</link>
          <guid>https://security.paloaltonetworks.com/CVE-2026-0288</guid>
          <description>PAN-OS security advisory</description>
          <pubDate>Wed, 08 Jul 2026 16:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>"""

    records = parse_registered_source(_source(), payload)

    assert len(records) == 1
    record = records[0]
    assert record.external_id == "https://security.paloaltonetworks.com/CVE-2026-0288"
    assert record.object_type == "security-advisory"
    assert record.title.startswith("CVE-2026-0288")
    assert record.url == "https://security.paloaltonetworks.com/CVE-2026-0288"
    assert record.source_reliability == "authoritative"
    assert record.raw["guid"] == record.external_id
    assert record.raw["description"] == "PAN-OS security advisory"
    assert record.raw["pubDate"] == "Wed, 08 Jul 2026 16:00:00 GMT"


def test_paloalto_rss_fails_closed_when_no_usable_items() -> None:
    payload = b"""<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'><channel><title>Palo Alto Networks Security Advisories</title></channel></rss>"""

    with pytest.raises(SourceExecutionError, match="RSS response has no channel items"):
        parse_registered_source(_source(), payload)
