from __future__ import annotations

from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import parse_registered_source
from dtmo.sources import SourceDefinition


def _debian_source() -> SourceDefinition:
    return SourceDefinition(
        id="debian-security",
        name="Debian Security Advisories",
        source_type="json-feed",
        endpoint_url="https://www.debian.org/security/dsa",
        enabled=True,
        interval_seconds=3600,
        reliability="authoritative",
        secret_ref=None,
        created_by="admin",
        updated_by="admin",
    )


def test_debian_catalog_entry_uses_governed_rss_profile() -> None:
    entry = catalog_by_id("debian-security")
    assert entry is not None
    assert entry.endpoint_url == "https://www.debian.org/security/dsa"
    assert entry.execution_status == "supported"
    assert entry.execution_profile == "rss-2.0"
    assert entry.reliability == "authoritative"


def test_debian_dsa_rss_normalizes_and_preserves_provenance() -> None:
    payload = b"""<?xml version='1.0' encoding='utf-8'?>
    <rss version='2.0'>
      <channel>
        <title>Debian Security Advisories</title>
        <item>
          <title>DSA-6424-1 xen security update</title>
          <link>https://www.debian.org/security/2026/dsa-6424</link>
          <guid>https://www.debian.org/security/2026/dsa-6424</guid>
          <description>Debian security update for xen.</description>
          <pubDate>Sun, 09 Aug 2026 00:00:00 UTC</pubDate>
        </item>
      </channel>
    </rss>"""

    records = parse_registered_source(_debian_source(), payload)

    assert len(records) == 1
    record = records[0]
    assert record.external_id == "https://www.debian.org/security/2026/dsa-6424"
    assert record.object_type == "security-advisory"
    assert record.title == "DSA-6424-1 xen security update"
    assert record.url == "https://www.debian.org/security/2026/dsa-6424"
    assert record.summary == "Debian security update for xen."
    assert record.source_reliability == "authoritative"
    assert record.raw["guid"] == record.external_id
    assert record.raw["pubDate"] == "Sun, 09 Aug 2026 00:00:00 UTC"
