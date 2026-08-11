from dtmo.source_catalog import catalog_by_id
from dtmo.source_executor import _parse_rss


def test_ubuntu_catalog_source_reuses_governed_rss_adapter() -> None:
    source = catalog_by_id("ubuntu-security-notices")
    assert source is not None
    assert source.execution_status == "supported"
    assert source.execution_profile == "rss-2.0"
    assert source.endpoint_url == "https://ubuntu.com/security/notices/rss.xml"
    assert source.reliability == "authoritative"


def test_ubuntu_rss_notice_normalizes_and_preserves_provenance() -> None:
    payload = b"""<?xml version='1.0' encoding='UTF-8'?>
    <rss version='2.0'><channel><title>Ubuntu Security Notices</title><item>
      <guid>https://ubuntu.com/security/notices/USN-8626-1</guid>
      <title>USN-8626-1: systemd vulnerabilities</title>
      <link>https://ubuntu.com/security/notices/USN-8626-1</link>
      <description>Several security issues were fixed in systemd.</description>
      <pubDate>Mon, 10 Aug 2026 12:00:00 GMT</pubDate>
    </item></channel></rss>"""
    records = _parse_rss(payload, "authoritative")
    assert len(records) == 1
    record = records[0]
    assert record.external_id.endswith("USN-8626-1")
    assert record.object_type == "security-advisory"
    assert record.title.startswith("USN-8626-1")
    assert record.url == "https://ubuntu.com/security/notices/USN-8626-1"
    assert record.source_reliability == "authoritative"
    assert record.raw["description"].startswith("Several security issues")
